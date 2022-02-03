from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class MainPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
    all_items_string = 'all'
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if page_size == self.all_items_string:
            page_size = len(queryset)
            if page_size < 1:
                page_size = self.page_size

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('page', self.page.number),
            ('page_size', self.page.paginator.per_page),
            ('last_page', self.page.paginator.num_pages),
            ('results', data)
        ]))

    def get_page_size(self, request):
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size == self.all_items_string:
            return page_size
        try:
            page_size = int(page_size)
        except Exception:
            return self.page_size

        if page_size < 1:
            return self.page_size
        if self.max_page_size and page_size > self.max_page_size:
            return self.max_page_size
        return page_size
