from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction
from .models import Listing
from .serializers import ListingSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny



#Bulk upload or bulk post to try multiple
class BulkListingView(APIView):
    """
    Handles both bulk and single listing creation.
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "category": openapi.Schema(type=openapi.TYPE_STRING),
                    "status": openapi.Schema(type=openapi.TYPE_STRING),
                    "city": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                },
                required=["title", "category"]
            ),
        ),
        responses={201: "Created", 400: "Bad Request"}
    )
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
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Filter by category",
                type=openapi.TYPE_STRING,
                enum=["apartment", "villa", "office", "land"]  # Dropdown values here
            ),
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filter by status",
                type=openapi.TYPE_STRING,
                enum=["available", "sold", "rented"]
            ),
            openapi.Parameter(
                'city', openapi.IN_QUERY, description="Filter by city name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Search text in title, city, description",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number",
                type=openapi.TYPE_INTEGER, default=1
            ),
            openapi.Parameter(
                'limit', openapi.IN_QUERY, description="Items per page",
                type=openapi.TYPE_INTEGER, default=10
            ),
        ],
        responses={200: ListingSerializer(many=True)}
    )

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
    
    
    @swagger_auto_schema(request_body=ListingSerializer)
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
    @swagger_auto_schema(request_body=ListingSerializer)
    def put(self, request, pk):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=ListingSerializer)
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
