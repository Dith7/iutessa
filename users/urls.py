from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('etudiant/', views.etudiant_dashboard, name='etudiant_dashboard'),
    
    # Profil utilisateur
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # Administration des utilisateurs (admin seulement)
    path('admin/users/', views.admin_users_list, name='admin_users_list'),
]