from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('administration/', include('administration.urls')),
    path('', include('pages.urls')),
    path('users/', include('users.urls')),
    path('academique/', include('academique.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]

# ====================
# 🔥 MEDIA - TOUJOURS SERVIR (pas de nginx dans votre setup)
# ====================
# Que ce soit en DEV ou en PROD, Django sert les media
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

# ====================
# STATIC & RELOAD (DEV uniquement)
# ====================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]