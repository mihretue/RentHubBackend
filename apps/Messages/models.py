from django.db import models
from django.conf import settings
from apps.Bookings.models import Booking
from apps.Listing.models import Listing
import uuid

User = settings.AUTH_USER_MODEL

class ConversationStatus(models.TextChoices):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    BLOCKED = "BLOCKED"

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="started_conversations")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_conversations")
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, blank=True, null=True)
    booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ConversationStatus.choices, default=ConversationStatus.ACTIVE)

class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_messages")
    content = models.TextField()
    was_filtered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
