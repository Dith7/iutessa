from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('administration/', include('administration.urls')),
    path('', include('pages.urls')),
    path('users/', include('users.urls')),
    path('academique/', include('academique.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]
