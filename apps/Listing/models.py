from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL



class Listing(models.Model):
    class Category(models.TextChoices):
        HOUSE = "HOUSE"
        APARTMENT = "APARTMENT"
        CABIN = "CABIN"
        VILLA = "VILLA"
        CAR = "CAR"
        BOAT = "BOAT"
        OTHER = "OTHER"
        OFFICE = "office"
        LAND = "land"

    class ListingStatus(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"
        PENDING = "PENDING"
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=Category.choices)
    price = models.FloatField()
    image_urls = models.TextField()
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ListingStatus.choices, default=ListingStatus.ACTIVE)
    featured = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")


    def __str__(self):
        return self.title
