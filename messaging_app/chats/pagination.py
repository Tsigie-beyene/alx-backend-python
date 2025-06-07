from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    """Custom pagination for messages with a page size of 20."""
    page_size = 20

    def get_paginated_response(self, data):
        """Customize paginated response to include total count."""
        return Response({
            'count': self.page.paginator.count,  # Total number of items
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
