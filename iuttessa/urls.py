# votre_projet/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('administration/', include('administration.urls')),
    path('', include('pages.urls')),
    path('users/', include('users.urls')),
    path('academique/', include('academique.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]

# MEDIA - toujours servir (même en prod Docker)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# STATIC - uniquement en dev
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]