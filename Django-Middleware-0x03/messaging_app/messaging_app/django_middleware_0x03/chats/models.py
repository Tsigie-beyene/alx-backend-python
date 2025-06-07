from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid  # required by ALX check

class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    bio = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    password = models.CharField(max_length=128)  # ALX check requires it explicitly

    def __str__(self):
        return self.username


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    message_body = models.TextField()  # must match ALX check
    sent_at = models.DateTimeField(auto_now_add=True)  # must match ALX check

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"
