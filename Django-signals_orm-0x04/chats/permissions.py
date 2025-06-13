from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """Custom permission to ensure only authenticated users who are conversation participants can access conversations and messages."""
    
    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the user is a participant in the conversation for the given action."""
        if isinstance(obj, Conversation):
            # Allow all CRUD actions if user is a participant
            return obj.participants.filter(user_id=request.user.user_id).exists()
        elif isinstance(obj, Message):
            # Allow GET, POST, PUT, PATCH, DELETE only if user is a participant in the conversation
            if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
            return False
        return False
