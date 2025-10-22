from rest_framework import serializers
from .models import Booking, Payment, PaymentNote, BookingStatus, PaymentStatus, PaymentMethod
from apps.Listing.models import Listing
from django.contrib.auth import get_user_model

User = get_user_model()


class BookingSerializer(serializers.ModelSerializer):
    renter = serializers.StringRelatedField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    listing_title = serializers.ReadOnlyField(source="listing.title")

    class Meta:
        model = Booking
        fields = [
            "id",
            "listing",
            "listing_title",
            "renter",
            "owner",
            "start_date",
            "end_date",
            "total_price",
            "status",
            "created_at",
            "updated_at",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    payer = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)
    booking_detail = BookingSerializer(source="booking", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "status",
            "payment_method",
            "payment_date",
            "created_at",
            "updated_at",
            "booking",
            "booking_detail",
            "payer",
            "receiver",
            "reference_code",
            "transaction_id",
            "metadata",
            "verified_by",
            "verified_at",
            "flagged",
            "flag_reason",
        ]


class PaymentNoteSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)
    payment_info = PaymentSerializer(source="payment", read_only=True)

    class Meta:
        model = PaymentNote
        fields = [
            "id",
            "content",
            "payment",
            "payment_info",
            "admin",
            "created_at",
        ]
