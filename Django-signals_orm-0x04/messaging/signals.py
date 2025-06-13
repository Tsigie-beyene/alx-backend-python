
# messaging/signals.py
from datetime import timezone
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Creates a notification when a new message is sent.
    """
    if created:
        Notification.objects.create(
            recipient=instance.receiver,
            sender=instance.sender,
            message=f"New message from {instance.sender.username}",
            content_object=instance  # Links to the Message
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Logs message edits by comparing old and new content.
    Creates a MessageHistory record when content changes.
    """
    if instance.pk:  # Only for existing messages (edits)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Content changed
                MessageHistory.objects.create(
                    original_message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
                instance.last_edited = timezone.now()
        except Message.DoesNotExist:
            pass  # New message being created



@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Cleans up all user-related data when a user is deleted.
    """
    # Delete all messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all message history where user edited messages
    MessageHistory.objects.filter(edited_by=instance).delete()
    
    # Delete all notifications where user is recipient or sender
    Notification.objects.filter(recipient=instance).delete()
    Notification.objects.filter(sender=instance).delete()        
