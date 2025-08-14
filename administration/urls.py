from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_view, name='dashboard'),
    
    # Gestion des blocs
    path('blocks/', views.blocks_list_view, name='blocks_list'),
    path('blocks/create/', views.block_create_view, name='block_create'),
    path('blocks/<int:pk>/', views.block_detail_view, name='block_detail'),
    path('blocks/<int:pk>/edit/', views.block_update_view, name='block_update'),
    path('blocks/<int:pk>/delete/', views.block_delete_view, name='block_delete'),
    
    # Actions AJAX sur les blocs
    path('blocks/<int:pk>/toggle-status/', views.block_toggle_status_view, name='block_toggle_status'),
    path('blocks/reorder/', views.blocks_reorder_view, name='blocks_reorder'),
    
    # Gestion des médias
    path('media/', views.media_library_view, name='media_library'),
    path('media/upload/', views.media_upload_view, name='media_upload'),
    
    # Utilitaires
    path('settings/', views.settings_view, name='settings'),
    path('preview/', views.preview_site_view, name='preview_site'),
    path('analytics/', views.analytics_view, name='analytics'),
]