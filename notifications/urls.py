# notifications/urls.py

from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Liste et détail
    path('', views.notification_list, name='list'),
    path('<int:pk>/', views.notification_detail, name='detail'),
    
    # Préférences
    path('preferences/', views.notification_preferences, name='preferences'),
    
    # Actions AJAX
    path('ajax/mark-read/', views.ajax_mark_as_read, name='ajax_mark_read'),
    path('ajax/mark-all-read/', views.ajax_mark_all_read, name='ajax_mark_all_read'),
    path('ajax/<int:pk>/delete/', views.ajax_delete_notification, name='ajax_delete'),
    path('ajax/unread-count/', views.ajax_unread_count, name='ajax_unread_count'),
    path('ajax/recent/', views.ajax_recent_notifications, name='ajax_recent'),
]