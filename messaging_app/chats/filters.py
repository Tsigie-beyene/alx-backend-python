from django_filters import rest_framework as filters
from chats.models import Message, User, Conversation

class MessageFilter(filters.FilterSet):
    """Filter for messages based on conversation participants."""
    participants = filters.ModelMultipleChoiceFilter(
        field_name='conversation__participants',
        queryset=User.objects.all(),
        label='Participants in the conversation'
    )
    sent_timestamp = filters.DateTimeFromToRangeFilter(
        field_name='sent_timestamp',
        label='Sent time range'
    )

    class Meta:
        model = Message
        fields = ['conversation', 'participants', 'sent_timestamp']
