from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('academic/', views.academic_overview, name='academic_overview'),
    path('documents/', views.documents_validation, name='documents_validation'),
    path('documents/<int:document_id>/validate/', views.validate_document, name='validate_document'),
    path('filieres/', views.filieres_management, name='filieres_management'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('settings/', views.settings_view, name='settings'),
]