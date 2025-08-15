from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserCreationFormWithRole, AdminUserEditForm

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Administration personnalisée pour le modèle User"""
    
    # Formulaires
    add_form = UserCreationFormWithRole
    form = AdminUserEditForm
    
    # Affichage de la liste
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    # Affichage détaillé
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'phone', 'date_of_birth')
        }),
    )
    
    # Formulaire d'ajout
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2'),
        }),
    )
    
    # Actions personnalisées
    actions = ['make_admin', 'make_etudiant', 'make_visiteur', 'activate_users', 'deactivate_users']
    
    def make_admin(self, request, queryset):
        """Action pour transformer les utilisateurs en admin"""
        updated = queryset.update(role='ADMIN')
        self.message_user(request, f'{updated} utilisateur(s) transformé(s) en administrateur.')
    make_admin.short_description = "Transformer en administrateur"
    
    def make_etudiant(self, request, queryset):
        """Action pour transformer les utilisateurs en étudiant"""
        updated = queryset.update(role='ETUDIANT')
        self.message_user(request, f'{updated} utilisateur(s) transformé(s) en étudiant.')
    make_etudiant.short_description = "Transformer en étudiant"
    
    def make_visiteur(self, request, queryset):
        """Action pour transformer les utilisateurs en visiteur"""
        updated = queryset.update(role='VISITEUR')
        self.message_user(request, f'{updated} utilisateur(s) transformé(s) en visiteur.')
    make_visiteur.short_description = "Transformer en visiteur"
    
    def activate_users(self, request, queryset):
        """Action pour activer les utilisateurs"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} utilisateur(s) activé(s).')
    activate_users.short_description = "Activer les utilisateurs"
    
    def deactivate_users(self, request, queryset):
        """Action pour désactiver les utilisateurs"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} utilisateur(s) désactivé(s).')
    deactivate_users.short_description = "Désactiver les utilisateurs"
    
    # Personnalisation de l'affichage
    def get_queryset(self, request):
        """Personnalise le queryset affiché"""
        qs = super().get_queryset(request)
        return qs.select_related()  # Optimisation des requêtes
    
    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression des superusers"""
        if obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)