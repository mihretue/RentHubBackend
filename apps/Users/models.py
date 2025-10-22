from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid



class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        RENTER = "RENTER", "Renter"
        OWNER = "OWNER", "Owner"
        ADMIN = "ADMIN", "Admin"

    class UserStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        DELETED = "DELETED", "Deleted"
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RENTER)
    status = models.CharField(max_length=20, choices=UserStatus.choices, default=UserStatus.ACTIVE)
    is_verified = models.BooleanField(default=False)
    verification_documents = models.TextField(blank=True, null=True)
    suspended_until = models.DateTimeField(blank=True, null=True)
    suspension_reason = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    document_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username or self.email or str(self.id)
