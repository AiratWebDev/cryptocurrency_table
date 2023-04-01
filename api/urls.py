from django.urls import path
from .views import CurrenciesAPIViewSet, CurrenciesBySymbolViewSet, api_links_page

urlpatterns = [
    path('links/', api_links_page, name='links'),

    path('currencies/', CurrenciesAPIViewSet.as_view({'get': 'list'}), name='api_currencies'),
    path('currencies/<int:pk>/', CurrenciesAPIViewSet.as_view({
        'put': 'update',
        'delete': 'destroy',
        'get': 'retrieve',
        'post': 'create'
    }), name='api_currencies_param'),
    path('currencies/symbol/<str:symbol>/', CurrenciesBySymbolViewSet.as_view(), name='api_symbol'),
]
