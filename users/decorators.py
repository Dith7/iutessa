from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def role_required(*allowed_roles):
    """
    Décorateur pour restreindre l'accès selon le rôle utilisateur
    
    Usage:
    @role_required('ADMIN')
    @role_required('ADMIN', 'ETUDIANT')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                messages.error(request, 'Accès non autorisé.')
                if request.user.is_admin():
                    return redirect('administration:dashboard')
                elif request.user.is_etudiant():
                    return redirect('users:etudiant_dashboard')
                else:
                    return redirect('pages:home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """Décorateur pour restreindre l'accès aux administrateurs uniquement"""
    return role_required('ADMIN')(view_func)


def etudiant_required(view_func):
    """Décorateur pour restreindre l'accès aux étudiants uniquement"""
    return role_required('ETUDIANT')(view_func)


def admin_or_etudiant_required(view_func):
    """Décorateur pour autoriser admin et étudiants"""
    return role_required('ADMIN', 'ETUDIANT')(view_func)


class RoleRequiredMixin:
    """
    Mixin pour les vues basées sur les classes
    
    Usage:
    class MyView(RoleRequiredMixin, TemplateView):
        required_roles = ['ADMIN', 'ETUDIANT']
    """
    required_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        if request.user.role not in self.required_roles:
            messages.error(request, 'Accès non autorisé.')
            if request.user.is_admin():
                return redirect('administration:dashboard')
            elif request.user.is_etudiant():
                return redirect('users:etudiant_dashboard')
            else:
                return redirect('pages:home')
        
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(RoleRequiredMixin):
    """Mixin pour restreindre aux administrateurs"""
    required_roles = ['ADMIN']


class EtudiantRequiredMixin(RoleRequiredMixin):
    """Mixin pour restreindre aux étudiants"""
    required_roles = ['ETUDIANT']


class AdminOrEtudiantRequiredMixin(RoleRequiredMixin):
    """Mixin pour autoriser admin et étudiants"""
    required_roles = ['ADMIN', 'ETUDIANT']