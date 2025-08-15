from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager to handle superuser creation with ADMIN role"""
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Create and return a regular user"""
        if not username:
            raise ValueError('Username is required')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and return a superuser with ADMIN role"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')  # Force ADMIN role for superuser
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Modèle utilisateur personnalisé avec système de rôles"""
    
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('ETUDIANT', 'Étudiant'),
        ('VISITEUR', 'Visiteur'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='VISITEUR',
        verbose_name='Rôle'
    )
    
    # Champs supplémentaires optionnels
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Téléphone'
    )
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de naissance'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use custom manager
    objects = UserManager()
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        """Vérifie si l'utilisateur est admin"""
        return self.role == 'ADMIN'
    
    def is_etudiant(self):
        """Vérifie si l'utilisateur est étudiant"""
        return self.role == 'ETUDIANT'
    
    def is_visiteur(self):
        """Vérifie si l'utilisateur est visiteur"""
        return self.role == 'VISITEUR'
    
    @property
    def full_name(self):
        """Retourne le nom complet"""
        return f"{self.first_name} {self.last_name}".strip() or self.username