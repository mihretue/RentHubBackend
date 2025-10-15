from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.name", read_only=True)
    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "category",
            "price",
            "image_urls",
            "address",
            "city",
            "state",
            "country",
            "features",
            "status",
            "featured",
            "flagged",
            "created_at",
            "updated_at",
            "owner",
            "owner_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "owner"]