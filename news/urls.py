from django.urls import path
from .views import news_page

urlpatterns = [
    path('', news_page, name='news')
]
