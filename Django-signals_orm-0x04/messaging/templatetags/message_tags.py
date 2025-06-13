# messaging/templatetags/message_tags.py
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_message_thread(message, depth=0):
    indent = '&nbsp;&nbsp;&nbsp;&nbsp;' * depth
    html = f"""
    <div class="message" style="margin-left: {depth * 20}px">
        <strong>{message.sender.username}</strong>
        <small>{message.timestamp}</small>
        <p>{message.content}</p>
    </div>
    """
    for reply in message.replies.all():
        html += render_message_thread(reply, depth + 1)
    return mark_safe(html)
