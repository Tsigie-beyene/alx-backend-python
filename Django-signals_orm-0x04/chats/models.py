import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Custom user model extending AbstractUser with additional fields."""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier for the user")
    email = models.EmailField(unique=True, help_text="User's email address")
    password = models.CharField(max_length=128, help_text="User's password")
    first_name = models.CharField(max_length=150, blank=True, help_text="User's first name")
    last_name = models.CharField(max_length=150, blank=True, help_text="User's last name")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="User's phone number")
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="Short user biography")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="User profile picture")
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

class Conversation(models.Model):
    """Model to represent a conversation between multiple users."""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier for the conversation")
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="Users participating in this conversation"
    )
    created_at = models.DateTimeField(default=timezone.now, help_text="When the conversation was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the conversation was last updated")

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.conversation_id} with {', '.join(participant.username for participant in self.participants.all())}"

class Message(models.Model):
    """Model to represent a message in a conversation."""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier for the message")
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message"
    )
    message_body = models.TextField(max_length=2000, help_text="Message content")
    sent_at = models.DateTimeField(default=timezone.now, help_text="When the message was sent")
    is_read = models.BooleanField(default=False, help_text="Whether the message has been read")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.username} in Conversation {self.conversation.conversation_id}"
