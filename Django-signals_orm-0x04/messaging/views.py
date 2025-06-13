
# accounts/views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from .models import Message
from django.db.models import Q, Prefetch
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This will trigger the post_delete signal
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    return render(request, 'accounts/confirm_delete.html')



@method_decorator(cache_page(60))  # Cache for 60 seconds
def conversation_view(request, recipient_id):
    """
    View for displaying a conversation thread between two users
    with optimized queries using select_related and prefetch_related
    """
    recipient = get_object_or_404(User, pk=recipient_id)
    
    # Base query with optimization
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=recipient) |
        Q(sender=recipient, receiver=request.user)
    ).select_related(
        'sender',
        'receiver',
        'parent_message'
    ).prefetch_related(
        Prefetch('replies', 
                queryset=Message.objects.select_related('sender', 'receiver')
                .order_by('timestamp'))
    ).order_by('timestamp')

    # Get root messages (messages without parents)
    root_messages = messages.filter(parent_message__isnull=True)

    context = {
        'recipient': recipient,
        'root_messages': root_messages,
    }
    return render(request, 'messaging/conversation.html', context)

@method_decorator(cache_page(60))  # Cache for 60 seconds
def message_thread(request, message_id):
    """
    View for displaying a single message thread with all replies
    using recursive fetching with optimized queries
    """
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver'),
        pk=message_id
    )

    # Get all messages in the thread (root + all replies)
    thread_messages = Message.objects.filter(
        Q(pk=root_message.pk) |
        Q(parent_message__pk=root_message.pk)
    ).select_related(
        'sender',
        'receiver'
    ).prefetch_related(
        Prefetch('replies',
                queryset=Message.objects.select_related('sender', 'receiver')
                .order_by('timestamp'))
    ).order_by('timestamp')

    context = {
        'root_message': root_message,
        'thread_messages': thread_messages,
    }
    return render(request, 'messaging/thread.html', context)




@login_required
@method_decorator(cache_page(60))  # Cache for 60 seconds
def unread_messages(request):
    """View showing only unread messages for the current user"""
    messages = Message.unread.unread_for_user(request.user).only(
            'message_id',
            'sender__username',
            'content',
            'timestamp'
        )
    
    return render(request, 'messaging/unread.html', {
        'unread_messages': messages,
        'unread_count': messages.count()  # Efficient count
    })



@require_POST
@login_required
def mark_as_read(request, message_id):
    """API endpoint to mark a message as read"""
    try:
        message = Message.objects.get(
            message_id=message_id,
            receiver=request.user
        )
        message.mark_as_read()
        return JsonResponse({'status': 'success'})
    except Message.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)
