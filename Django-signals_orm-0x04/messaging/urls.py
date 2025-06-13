# accounts/urls.py
from django.urls import path
from .views import delete_user, unread_messages, mark_as_read

urlpatterns = [
    path('delete/', delete_user, name='delete_user'),
    path('unread/', unread_messages, name='unread_messages'),
    path('<uuid:message_id>/mark-read/', mark_as_read, name='mark_as_read'),
]
