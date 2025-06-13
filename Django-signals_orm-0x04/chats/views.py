# chats/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsParticipantOfConversation
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating conversations with filtering."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']

    @method_decorator(cache_page(60))  # Cache for 60 seconds
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new conversation and add the requesting user as a participant."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            conversation.participants.add(self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """Return conversations where the user is a participant."""
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and sending messages with filtering."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']

    @method_decorator(cache_page(60))  # Cache for 60 seconds
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new message with the requesting user as sender, using conversation from URL."""
        conversation_id = self.kwargs.get('conversation_conversation_id')
        if not conversation_id:
            return Response({"detail": "Conversation ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            if not conversation.participants.filter(user_id=request.user.user_id).exists():
                return Response({"detail": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation does not exist."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['conversation'] = conversation.conversation_id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """Return messages from conversations the user is part of."""
        queryset = Message.objects.filter(conversation__participants=self.request.user)
        conversation_id = self.kwargs.get('conversation_conversation_id') or self.request.query_params.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset
