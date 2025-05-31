from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, excluding sensitive fields like password."""
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'bio', 'profile_picture']
        read_only_fields = ['user_id']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model, with sender and conversation as nested representations."""
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)
    message_body = serializers.CharField(max_length=2000, help_text="Message content")

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'is_read']
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model, including nested participants and messages."""
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    def get_messages(self, obj):
        """Custom method to serialize messages for the conversation."""
        messages = obj.messages.all()  # Access via related_name
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        """Ensure a conversation has at least two participants."""
        if 'participants' in data and len(data['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data
