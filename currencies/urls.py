from django.urls import path
from .views import currencies_page, SearchCurrencyView, synchronize_currencies_info

urlpatterns = [
    path('', currencies_page, name='main'),
    path('search/', SearchCurrencyView.as_view(), name='search'),
    path('sync/', synchronize_currencies_info, name='sync'),
]