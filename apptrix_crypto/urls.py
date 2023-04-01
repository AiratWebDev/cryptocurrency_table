from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('news/', include('news.urls')),
    path('favorites/', include('favorites.urls')),
    path('', include('currencies.urls')),
    path('', include('users.urls')),
]
