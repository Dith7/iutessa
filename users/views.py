from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from .forms import CustomLoginForm, UserProfileForm
from .decorators import role_required


def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.full_name}!')
                
                # Redirection selon le rôle
                if user.is_admin():
                    return redirect('administration:dashboard')
                elif user.is_etudiant():
                    return redirect('users:etudiant_dashboard')
                else:
                    return redirect('pages:home')
            else:
                messages.error(request, 'Identifiants incorrects.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('pages:home')


@login_required
def dashboard_view(request):
    """Dashboard principal après connexion"""
    user = request.user
    
    context = {
        'user': user,
        'recent_activity': _get_user_recent_activity(user),
    }
    
    # Template différent selon le rôle
    if user.is_admin():
        return redirect('administration:dashboard')
    elif user.is_etudiant():
        return render(request, 'users/etudiant_dashboard.html', context)
    else:
        return render(request, 'users/visiteur_dashboard.html', context)


@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})


@login_required
def change_password_view(request):
    """Vue pour changer le mot de passe"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour garder la session
            messages.success(request, 'Mot de passe changé avec succès.')
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})


@role_required('ADMIN')
def admin_users_list(request):
    """Liste des utilisateurs (admin seulement)"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
        'total_users': users.count(),
        'admin_count': users.filter(role='ADMIN').count(),
        'etudiant_count': users.filter(role='ETUDIANT').count(),
        'visiteur_count': users.filter(role='VISITEUR').count(),
    }
    
    return render(request, 'users/admin_users_list.html', context)


@role_required('ETUDIANT')
def etudiant_dashboard(request):
    """Dashboard spécifique aux étudiants"""
    context = {
        'user': request.user,
        'notifications': _get_etudiant_notifications(request.user),
        'academic_info': _get_academic_info(request.user),
    }
    
    return render(request, 'users/etudiant_dashboard.html', context)


# Fonctions utilitaires
def _get_user_recent_activity(user):
    """Récupère l'activité récente de l'utilisateur"""
    # À implémenter selon les besoins
    return []


def _get_etudiant_notifications(user):
    """Récupère les notifications pour un étudiant"""
    # À implémenter selon les besoins
    return []


def _get_academic_info(user):
    """Récupère les informations académiques d'un étudiant"""
    # À implémenter selon les besoins
    return {}