from django.db import models
from django.conf import settings
from apps.Listing.models import Listing
import uuid

User = settings.AUTH_USER_MODEL

class BookingStatus(models.TextChoices):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.FloatField()
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="renter_bookings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_bookings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")

    def __str__(self):
        return f"{self.listing.title} ({self.status})"

class PaymentMethod(models.TextChoices):
    CARD = "CARD"
    TELEBIRR = "TELEBIRR"
    CBE = "CBE"
    CASH = "CASH"
    OTHER = "OTHER"

class PaymentStatus(models.TextChoices):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    VERIFIED = "VERIFIED"
    FLAGGED = "FLAGGED"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CARD)
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_payments")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_payments")
    reference_code = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    verified_by = models.CharField(max_length=100, blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    flagged = models.BooleanField(default=False)
    flag_reason = models.TextField(blank=True, null=True)

class PaymentNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="notes")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_notes")
