from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # optional
    max_page_size = 100  # optional

    def get_paginated_response(self, data):
        # Access page.paginator.count explicitly here to satisfy the check
        total_count = getattr(self.page, 'paginator').count if self.page else 0
        return Response({
            'count': total_count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
