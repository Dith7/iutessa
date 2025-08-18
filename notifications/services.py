# notifications/services.py

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from .models import Notification, PreferenceNotification
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class NotificationService:
    """Service principal pour gérer les notifications et emails"""
    
    @staticmethod
    def create_notification(
        destinataire, 
        type_notification, 
        titre, 
        message,
        expediteur=None,
        priorite='normale',
        url_action='',
        send_email=True
    ):
        """
        Crée une notification et envoie un email si nécessaire
        """
        try:
            # Créer la notification
            notification = Notification.objects.create(
                destinataire=destinataire,
                expediteur=expediteur,
                type_notification=type_notification,
                priorite=priorite,
                titre=titre,
                message=message,
                url_action=url_action
            )
            
            # Vérifier les préférences et envoyer l'email
            if send_email:
                preferences = NotificationService.get_user_preferences(destinataire)
                if NotificationService.should_send_email(preferences, type_notification):
                    NotificationService.send_email_notification(notification)
                    notification.email_envoye = True
                    notification.save()
            
            return notification
            
        except Exception as e:
            logger.error(f"Erreur création notification: {e}")
            return None
    
    @staticmethod
    def get_user_preferences(user):
        """Récupère ou crée les préférences de notification d'un utilisateur"""
        preferences, created = PreferenceNotification.objects.get_or_create(user=user)
        return preferences
    
    @staticmethod
    def should_send_email(preferences, type_notification):
        """Détermine si un email doit être envoyé selon les préférences"""
        if not preferences:
            return True
        
        type_mapping = {
            'inscription_complete': preferences.email_inscription,
            'inscription_validee': preferences.email_inscription,
            'inscription_rejetee': preferences.email_inscription,
            'document_upload': preferences.email_documents,
            'document_valide': preferences.email_documents,
            'document_rejete': preferences.email_documents,
            'document_manquant': preferences.email_documents,
            'profil_complete': preferences.email_validation,
            'profil_incomplet': preferences.email_validation,
            'validation_profil': preferences.email_validation,
            'rappel': preferences.email_rappels,
            'info': preferences.email_info,
        }
        
        return type_mapping.get(type_notification, True)
    
    @staticmethod
    def send_email_notification(notification):
        """Envoie un email HTML pour une notification"""
        try:
            context = {
                'notification': notification,
                'user': notification.destinataire,
                'site_name': 'IUT-ESSA',
                'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
            }
            
            # Sélectionner le template selon le type
            template_name = NotificationService.get_email_template(notification.type_notification)
            
            # Générer le contenu HTML et texte
            html_content = render_to_string(f'notifications/emails/{template_name}', context)
            text_content = strip_tags(html_content)
            
            # Créer et envoyer l'email
            email = EmailMultiAlternatives(
                subject=f"[IUT-ESSA] {notification.titre}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[notification.destinataire.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            
            logger.info(f"Email envoyé à {notification.destinataire.email}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur envoi email: {e}")
            return False
    
    @staticmethod
    def get_email_template(type_notification):
        """Retourne le template approprié selon le type de notification"""
        templates = {
            'inscription_complete': 'inscription_complete.html',
            'inscription_validee': 'inscription_validee.html',
            'inscription_rejetee': 'inscription_rejetee.html',
            'document_valide': 'document_valide.html',
            'document_rejete': 'document_rejete.html',
            'document_manquant': 'document_manquant.html',
            'rappel': 'rappel.html',
        }
        return templates.get(type_notification, 'default.html')
    
    @staticmethod
    def notify_inscription_complete(etudiant):
        """Notification quand un étudiant complète son inscription"""
        return NotificationService.create_notification(
            destinataire=etudiant.user,
            type_notification='inscription_complete',
            titre='Inscription complétée avec succès',
            message=f'Félicitations {etudiant.prenoms}, votre inscription académique a été enregistrée. '
                   f'Votre matricule est : {etudiant.numero_matricule}',
            priorite='haute',
            url_action='/academique/profil/'
        )
    
    @staticmethod
    def notify_inscription_validated(etudiant, validateur):
        """Notification quand une inscription est validée"""
        return NotificationService.create_notification(
            destinataire=etudiant.user,
            expediteur=validateur,
            type_notification='inscription_validee',
            titre='Votre inscription a été validée',
            message=f'Votre inscription en {etudiant.filiere.nom} a été validée. '
                   f'Vous pouvez maintenant accéder à tous les services.',
            priorite='haute',
            url_action='/academique/profil/'
        )
    
    @staticmethod
    def notify_document_validated(document, validateur):
        """Notification quand un document est validé"""
        return NotificationService.create_notification(
            destinataire=document.etudiant.user,
            expediteur=validateur,
            type_notification='document_valide',
            titre=f'Document validé : {document.get_type_document_display()}',
            message=f'Votre document "{document.get_type_document_display()}" a été validé avec succès.',
            priorite='normale',
            url_action='/academique/documents/'
        )
    
    @staticmethod
    def notify_document_rejected(document, validateur, raison=''):
        """Notification quand un document est rejeté"""
        message = f'Votre document "{document.get_type_document_display()}" a été rejeté.'
        if raison:
            message += f'\nRaison : {raison}'
        message += '\nVeuillez soumettre un nouveau document.'
        
        return NotificationService.create_notification(
            destinataire=document.etudiant.user,
            expediteur=validateur,
            type_notification='document_rejete',
            titre=f'Document rejeté : {document.get_type_document_display()}',
            message=message,
            priorite='haute',
            url_action='/academique/documents/'
        )
    
    @staticmethod
    def notify_documents_missing(etudiant, documents_manquants):
        """Notification de rappel pour documents manquants"""
        if not documents_manquants:
            return None
        
        docs_list = ', '.join([doc for doc in documents_manquants])
        
        return NotificationService.create_notification(
            destinataire=etudiant.user,
            type_notification='document_manquant',
            titre='Documents manquants',
            message=f'Il vous manque les documents suivants : {docs_list}. '
                   f'Veuillez les soumettre pour compléter votre dossier.',
            priorite='haute',
            url_action='/academique/documents/'
        )
    
    @staticmethod
    def notify_import_success(users_imported, admin_user):
        """Notification pour chaque étudiant importé"""
        notifications = []
        for user in users_imported:
            notification = NotificationService.create_notification(
                destinataire=user,
                expediteur=admin_user,
                type_notification='import_success',
                titre='Votre compte a été créé',
                message='Votre compte étudiant a été créé suite à l\'import de vos données. '
                       'Veuillez vous connecter pour vérifier et compléter votre inscription. '
                       'Mot de passe temporaire : password123',
                priorite='urgente',
                url_action='/login/'
            )
            notifications.append(notification)
        return notifications
    
    @staticmethod
    def bulk_notify(users, type_notification, titre, message, expediteur=None):
        """Envoie une notification à plusieurs utilisateurs"""
        notifications = []
        for user in users:
            notification = NotificationService.create_notification(
                destinataire=user,
                expediteur=expediteur,
                type_notification=type_notification,
                titre=titre,
                message=message
            )
            notifications.append(notification)
        return notifications