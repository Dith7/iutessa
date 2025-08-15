from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()


@receiver(post_save, sender=User)
def assign_role_permissions(sender, instance, created, **kwargs):
    """
    Assigne automatiquement les permissions selon le rôle de l'utilisateur
    """
    if created:
        # Créer les groupes s'ils n'existent pas
        admin_group, _ = Group.objects.get_or_create(name='Administrateurs')
        etudiant_group, _ = Group.objects.get_or_create(name='Étudiants')
        visiteur_group, _ = Group.objects.get_or_create(name='Visiteurs')
        
        # Assigner l'utilisateur au bon groupe selon son rôle
        if instance.role == 'ADMIN':
            instance.groups.add(admin_group)
            instance.is_staff = True
            instance.save()
        elif instance.role == 'ETUDIANT':
            instance.groups.add(etudiant_group)
        elif instance.role == 'VISITEUR':
            instance.groups.add(visiteur_group)


@receiver(post_save, sender=User)
def setup_user_permissions(sender, instance, created, **kwargs):
    """
    Configure les permissions spécifiques selon le rôle
    """
    if not created:
        return
    
    # Permissions pour les administrateurs
    if instance.role == 'ADMIN':
        # Les admins ont accès à tout
        all_permissions = Permission.objects.all()
        instance.user_permissions.set(all_permissions)
    
    # Permissions pour les étudiants
    elif instance.role == 'ETUDIANT':
        # Permissions spécifiques aux étudiants
        etudiant_permissions = Permission.objects.filter(
            codename__in=[
                'view_user',  # Voir son propre profil
                'change_user',  # Modifier son propre profil
            ]
        )
        instance.user_permissions.set(etudiant_permissions)
    
    # Permissions pour les visiteurs
    elif instance.role == 'VISITEUR':
        # Permissions minimales pour les visiteurs
        visiteur_permissions = Permission.objects.filter(
            codename__in=[
                'view_user',  # Voir son propre profil
            ]
        )
        instance.user_permissions.set(visiteur_permissions)


def create_default_groups():
    """
    Crée les groupes par défaut avec leurs permissions
    """
    # Groupe Administrateurs
    admin_group, created = Group.objects.get_or_create(name='Administrateurs')
    if created:
        # Tous les permissions pour les admins
        admin_group.permissions.set(Permission.objects.all())
    
    # Groupe Étudiants
    etudiant_group, created = Group.objects.get_or_create(name='Étudiants')
    if created:
        etudiant_permissions = Permission.objects.filter(
            codename__in=[
                'view_user',
                'change_user',
            ]
        )
        etudiant_group.permissions.set(etudiant_permissions)
    
    # Groupe Visiteurs
    visiteur_group, created = Group.objects.get_or_create(name='Visiteurs')
    if created:
        visiteur_permissions = Permission.objects.filter(
            codename__in=[
                'view_user',
            ]
        )
        visiteur_group.permissions.set(visiteur_permissions)