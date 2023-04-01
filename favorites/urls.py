from django.urls import path
from .views import favorites_page, add_or_delete_to_favorites

urlpatterns = [
    path('', favorites_page, name='favorites'),
    path('to-favorites/', add_or_delete_to_favorites, name='to-favorites'),
    path('out-of-favorites/', add_or_delete_to_favorites, name='out-of-favorites'),
]
