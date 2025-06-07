from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation
    for viewing and modifying messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Viewing: GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()

        # Modifying: POST, PUT, PATCH, DELETE
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()

        return False
