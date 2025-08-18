# notifications/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    """Modèle pour les notifications internes à l'application"""

    TYPE_NOTIFICATION_CHOICES = [
        # Académique
        ('inscription_complete', 'Inscription complétée'),
        ('inscription_validee', 'Inscription validée'),
        ('inscription_rejetee', 'Inscription rejetée'),
        
        # Documents
        ('document_upload', 'Document téléchargé'),
        ('document_valide', 'Document validé'),
        ('document_rejete', 'Document rejeté'),
        ('document_manquant', 'Document manquant'),
        
        # Profil
        ('profil_complete', 'Profil complété'),
        ('profil_incomplet', 'Profil incomplet'),
        ('validation_profil', 'Validation du profil'),
        
        # Import
        ('import_success', 'Import réussi'),
        ('import_error', 'Erreur d\'import'),
        
        # Système
        ('rappel', 'Rappel'),
        ('info', 'Information'),
        ('alerte', 'Alerte'),
        ('autre', 'Autre'),
    ]

    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('normale', 'Normale'),
        ('haute', 'Haute'),
        ('urgente', 'Urgente'),
    ]

    destinataire = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Destinataire"
    )
    expediteur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications_envoyees',
        verbose_name="Expéditeur"
    )
    type_notification = models.CharField(
        max_length=50,
        choices=TYPE_NOTIFICATION_CHOICES,
        default='info',
        verbose_name="Type de notification"
    )
    priorite = models.CharField(
        max_length=10,
        choices=PRIORITE_CHOICES,
        default='normale',
        verbose_name="Priorité"
    )
    titre = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )
    message = models.TextField(verbose_name="Message")
    url_action = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="URL d'action"
    )
    lu = models.BooleanField(default=False, verbose_name="Lu")
    email_envoye = models.BooleanField(default=False, verbose_name="Email envoyé")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['destinataire', 'lu']),
            models.Index(fields=['type_notification']),
        ]

    def __str__(self):
        return f"{self.titre} - {self.destinataire.username}"
    
    def marquer_comme_lu(self):
        """Marque la notification comme lue"""
        if not self.lu:
            self.lu = True
            self.date_lecture = timezone.now()
            self.save()
    
    @property
    def est_urgente(self):
        return self.priorite in ['haute', 'urgente']
    
    @property
    def icone(self):
        """Retourne l'icône appropriée selon le type"""
        icons = {
            'inscription_complete': 'fa-check-circle text-green-600',
            'inscription_validee': 'fa-user-check text-green-600',
            'inscription_rejetee': 'fa-user-times text-red-600',
            'document_upload': 'fa-file-upload text-blue-600',
            'document_valide': 'fa-file-check text-green-600',
            'document_rejete': 'fa-file-times text-red-600',
            'document_manquant': 'fa-file-medical text-yellow-600',
            'profil_complete': 'fa-user-circle text-green-600',
            'profil_incomplet': 'fa-user-edit text-yellow-600',
            'validation_profil': 'fa-user-shield text-blue-600',
            'import_success': 'fa-file-import text-green-600',
            'import_error': 'fa-file-excel text-red-600',
            'rappel': 'fa-bell text-yellow-600',
            'info': 'fa-info-circle text-blue-600',
            'alerte': 'fa-exclamation-triangle text-red-600',
            'autre': 'fa-envelope text-gray-600',
        }
        return icons.get(self.type_notification, 'fa-bell text-gray-600')


class PreferenceNotification(models.Model):
    """Préférences de notification par utilisateur"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='preferences_notification'
    )
    
    # Préférences email
    email_inscription = models.BooleanField(default=True, verbose_name="Email pour inscription")
    email_documents = models.BooleanField(default=True, verbose_name="Email pour documents")
    email_validation = models.BooleanField(default=True, verbose_name="Email pour validation")
    email_rappels = models.BooleanField(default=True, verbose_name="Email pour rappels")
    email_info = models.BooleanField(default=False, verbose_name="Email pour informations")
    
    # Préférences notification push
    push_enabled = models.BooleanField(default=True, verbose_name="Notifications push activées")
    
    # Fréquence
    FREQUENCE_CHOICES = [
        ('immediate', 'Immédiate'),
        ('daily', 'Quotidienne'),
        ('weekly', 'Hebdomadaire'),
    ]
    frequence_email = models.CharField(
        max_length=10,
        choices=FREQUENCE_CHOICES,
        default='immediate',
        verbose_name="Fréquence des emails"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Préférence de notification"
        verbose_name_plural = "Préférences de notification"
    
    def __str__(self):
        return f"Préférences de {self.user.username}"