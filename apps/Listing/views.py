from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction
from .models import Listing
from .serializers import ListingSerializer

#Bulk upload or bulk post to try multiple
class BulkListingView(APIView):
    """
    Handles both bulk and single listing creation.
    """

    def post(self, request):
        data = request.data

        # ✅ Ensure we’re working with a list
        if isinstance(data, dict):
            # Single object — wrap in a list
            data = [data]
        elif not isinstance(data, list):
            return Response(
                {"error": "Expected a JSON object or a list of objects."},
                status=status.HTTP_400_BAD_REQUEST
            )

        created = []
        errors = []

        # ✅ Wrap operations in a transaction
        with transaction.atomic():
            for item in data:
                # Add owner if authenticated
                if request.user.is_authenticated:
                    item["owner"] = request.user.id

                serializer = ListingSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                    created.append(serializer.data)
                else:
                    errors.append(serializer.errors)

        return Response(
            {
                "created_count": len(created),
                "created": created,
                "errors": errors,
            },
            status=status.HTTP_201_CREATED
        )
class ListingAPIView(APIView):
    """
    Handles GET (list + filter + pagination), POST (create)
    """

    def get(self, request):
        # Filtering params
        category = request.GET.get("category")
        status_param = request.GET.get("status")
        city = request.GET.get("city")
        search = request.GET.get("search")
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))

        listings = Listing.objects.all().order_by("-created_at")

        # Apply filters
        if category:
            listings = listings.filter(category=category)
        if status_param:
            listings = listings.filter(status=status_param)
        if city:
            listings = listings.filter(city__icontains=city)
        if search:
            listings = listings.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(city__icontains=search)
            )

        # Pagination
        paginator = Paginator(listings, limit)
        paginated_listings = paginator.get_page(page)

        serializer = ListingSerializer(paginated_listings, many=True)
        response_data = {
            "results": serializer.data,
            "total": paginator.count,
            "page": page,
            "pages": paginator.num_pages,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Handle both single and multiple JSON objects
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            return Response(
                {"error": "Expected a JSON object or a list of objects."},
                status=status.HTTP_400_BAD_REQUEST
            )

        created = []
        errors = []

        with transaction.atomic():
            for item in data:
                if request.user.is_authenticated:
                    item["owner"] = request.user.id

                serializer = ListingSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                    created.append(serializer.data)
                else:
                    errors.append(serializer.errors)

        return Response(
            {
                "created_count": len(created),
                "created": created,
                "errors": errors,
            },
            status=status.HTTP_201_CREATED
        )



class ListingDetailAPIView(APIView):
    """
    Handles GET (single), PUT/PATCH (update), DELETE
    """

    def get_object(self, pk):
        return get_object_or_404(Listing, pk=pk)

    def get(self, request, pk):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        listing = self.get_object(pk)
        listing.delete()
        return Response({"message": "Listing deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
