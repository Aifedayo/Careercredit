from collections import OrderedDict

from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator    

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,self.request, view=self) 

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class PaginatedChatMessage(CursorPagination):

    # page_size = 30 #---crucial line
    # max_page_size = 1000

    def get_paginated_response(self, data, active_group):
        return Response(OrderedDict([
            # ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('active_group', active_group), #custom field
            ('results', data)
        ]))
