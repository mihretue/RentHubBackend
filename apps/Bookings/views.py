from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Booking, Payment, PaymentNote, PaymentStatus
from .serializers import BookingSerializer, PaymentSerializer, PaymentNoteSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related("renter", "owner", "listing")
    serializer_class = BookingSerializer
   

    def perform_create(self, serializer):
        # Automatically assign renter as the logged-in user
        serializer.save(renter=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().select_related("booking", "payer", "receiver")
    serializer_class = PaymentSerializer

 
     #  Add filtering and searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "booking"]  # filter by status & booking id
    search_fields = ["reference_code", "transaction_id"]  # optional
    ordering_fields = ["created_at", "amount", "payment_date"]

    def perform_create(self, serializer):
        serializer.save(payer=self.request.user)

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        """Mark payment as verified"""
        payment = self.get_object()
        payment.status = PaymentStatus.VERIFIED
        payment.verified_by = request.user.username
        payment.verified_at = timezone.now()
        payment.save()
        return Response({"message": "Payment verified successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def flag(self, request, pk=None):
        """Flag a payment for review"""
        payment = self.get_object()
        reason = request.data.get("reason", "No reason provided")
        payment.flagged = True
        payment.flag_reason = reason
        payment.status = PaymentStatus.FLAGGED
        payment.save()
        return Response({"message": "Payment flagged successfully"}, status=status.HTTP_200_OK)


class PaymentNoteViewSet(viewsets.ModelViewSet):
    queryset = PaymentNote.objects.all().select_related("payment", "admin")
    serializer_class = PaymentNoteSerializer

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)
