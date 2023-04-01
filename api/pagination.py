from rest_framework.pagination import PageNumberPagination


class CurrenciesAPIListPagination(PageNumberPagination):
    """Class for pagination setup"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500
