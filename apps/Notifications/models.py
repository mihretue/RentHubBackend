from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class NotificationType(models.TextChoices):
    INFO = "INFO"
    WARNING = "WARNING"
    ALERT = "ALERT"
    SUCCESS = "SUCCESS"

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.INFO)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
