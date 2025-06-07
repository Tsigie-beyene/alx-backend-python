import logging
from datetime import datetime, timedelta
from pathlib import Path
from django.http import HttpResponseForbidden, HttpResponse
from threading import Lock

# Configure logger for RequestLoggingMiddleware
logging.basicConfig(
    filename=str(Path(__file__).resolve().parent.parent.parent / 'requests.log'),
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    """Middleware to log user requests with timestamp, user, and path."""
    
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Log the request details and process the request."""
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to the app outside 6 PM to 9 PM."""
    
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Check server time and deny access outside 6 PM to 9 PM."""
        current_hour = datetime.now().hour
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to the messaging app is restricted outside 6 PM to 9 PM.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    """Middleware to limit chat messages to 5 per minute per IP address."""
    
    _request_counts = {}
    _lock = Lock()
    
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Check POST request rate limit per IP address."""
        if request.method == 'POST' and 'conversations' in request.path and 'messages' in request.path:
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            if ip_address:
                ip_address = ip_address.split(',')[0].strip()

            with self._lock:
                now = datetime.now()
                if ip_address in self._request_counts:
                    self._request_counts[ip_address] = [
                        timestamp for timestamp in self._request_counts[ip_address]
                        if now - timestamp < timedelta(minutes=1)
                    ]
                else:
                    self._request_counts[ip_address] = []

                if len(self._request_counts[ip_address]) >= 5:
                    return HttpResponse(
                        "Rate limit exceeded: 5 messages per minute allowed.",
                        status=429
                    )

                self._request_counts[ip_address].append(now)

        return self.get_response(request)

class RolepermissionMiddleware:
    """Middleware to restrict access to admin or moderator roles."""
    
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Check if user has admin or moderator role, except for token endpoints."""
        if request.path in ['/api/token/', '/api/token/refresh/']:
            return self.get_response(request)
        
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required.")
        
        if request.user.role not in ['admin', 'moderator']:
            return HttpResponseForbidden("Access restricted to admin or moderator roles.")
        
        return self.get_response(request)
