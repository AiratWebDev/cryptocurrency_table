from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

from currencies.models import Currency
from .serializers import CurrencySerializer
from .pagination import CurrenciesAPIListPagination


class CurrenciesAPIViewSet(viewsets.ModelViewSet):
    """Class based view to provide get, post, patch, delete methods for currency by id"""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = CurrenciesAPIListPagination


class CurrenciesBySymbolViewSet(APIView):
    """Class based view for api endpoint to get currency by its symbol"""

    def get(self, request, symbol=None):
        try:
            currency = Currency.objects.get(symbol__iexact=symbol)
            serializer = CurrencySerializer(currency)
            return Response(serializer.data)

        except Exception as error:
            return Response({'Error': f'{error}'})


def api_links_page(request):
    """View for page with list of all api links"""
    return render(request, 'api/links_page.html')
