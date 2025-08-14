from django.db import models
from django.core.validators import FileExtensionValidator
import os

from django.forms import ValidationError

# Essayer d'importer CKEditor 5, sinon utiliser TextField basique
try:
    from django_ckeditor_5.fields import CKEditor5Field
    CKEDITOR_AVAILABLE = True
except ImportError:
    CKEDITOR_AVAILABLE = False

def validate_file_size(value):
    """Valider la taille des fichiers (max 50MB)"""
    filesize = value.size
    if filesize > 50 * 1024 * 1024:  # 50MB
        raise ValidationError("La taille du fichier ne peut pas dépasser 50MB.")
    return value

def document_upload_path(instance, filename):
    """Chemin d'upload pour les documents"""
    return f'documents/{instance.block_type}/{filename}'

def video_upload_path(instance, filename):
    """Chemin d'upload pour les vidéos"""
    return f'videos/{instance.block_type}/{filename}'

class PageBlock(models.Model):
    BLOCK_TYPES = [
        ('hero', 'Section Hero'),
        ('about', 'À Propos'),
        ('contact', 'Contact'),
        ('news', 'Communiqués/Actualités'),
        ('gallery', 'Galerie Photos'),
        ('documents', 'Documents/Fichiers'),
        ('videos', 'Vidéos'),
        ('testimonials', 'Témoignages'),
        ('services', 'Services'),
        ('stats', 'Statistiques'),
        ('team', 'Notre Équipe'),
        ('custom', 'Contenu Personnalisé'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('inactive', 'Inactif'),
    ]
    
    VIDEO_TYPES = [
        ('local', 'Vidéo locale (upload)'),
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('embed', 'Code d\'intégration'),
    ]
    
    # Champs de base
    title = models.CharField(max_length=200, verbose_name="Titre")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    
    # Contenu
    if CKEDITOR_AVAILABLE:
        content = CKEditor5Field('Contenu', config_name='default', blank=True)
    else:
        content = models.TextField(
            verbose_name="Contenu", 
            blank=True,
            help_text="HTML basique autorisé"
        )
    
    block_type = models.CharField(
        max_length=50, 
        choices=BLOCK_TYPES, 
        default='custom',
        verbose_name="Type de bloc"
    )
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name="Statut"
    )
    
    # Média existant
    image = models.ImageField(
        upload_to='blocks/images/', 
        blank=True, 
        null=True, 
        verbose_name="Image",
        help_text="Image principale du bloc"
    )
    
    # NOUVEAUX CHAMPS - Documents
    document = models.FileField(
        upload_to=document_upload_path,
        blank=True,
        null=True,
        verbose_name="Document",
        help_text="PDF, Word, Excel, PowerPoint, etc.",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf']
            ),
            validate_file_size
        ]
    )
    
    document_title = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Titre du document",
        help_text="Nom affiché pour le téléchargement"
    )
    
    # NOUVEAUX CHAMPS - Vidéos
    video_type = models.CharField(
        max_length=20,
        choices=VIDEO_TYPES,
        default='local',
        verbose_name="Type de vidéo"
    )
    
    video_file = models.FileField(
        upload_to=video_upload_path,
        blank=True,
        null=True,
        verbose_name="Fichier vidéo",
        help_text="Pour vidéos locales (MP4, WebM) - Max 50MB",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['mp4', 'webm', 'avi', 'mov']
            ),
            validate_file_size
        ]
    )
    
    video_url = models.URLField(
        blank=True,
        verbose_name="URL de la vidéo",
        help_text="URL YouTube, Vimeo ou autre"
    )
    
    video_embed_code = models.TextField(
        blank=True,
        verbose_name="Code d'intégration",
        help_text="Code iframe ou embed pour vidéos externes"
    )
    
    video_thumbnail = models.ImageField(
        upload_to='videos/thumbnails/',
        blank=True,
        null=True,
        verbose_name="Miniature vidéo",
        help_text="Image de prévisualisation"
    )
    
    # Liens
    link_url = models.URLField(blank=True, verbose_name="Lien (optionnel)")
    link_text = models.CharField(max_length=100, blank=True, verbose_name="Texte du lien")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Bloc de page"
        verbose_name_plural = "Blocs de page"
    
    def __str__(self):
        return f"{self.title} ({self.get_block_type_display()})"
    
    def get_document_name(self):
        """Retourne le nom du document pour l'affichage"""
        if self.document_title:
            return self.document_title
        elif self.document:
            return os.path.basename(self.document.name)
        return "Document"
    
    def get_document_extension(self):
        """Retourne l'extension du document"""
        if self.document:
            return os.path.splitext(self.document.name)[1].upper().replace('.', '')
        return ""
    
    def get_document_size(self):
        """Retourne la taille du document formatée"""
        if self.document:
            size = self.document.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size // 1024} KB"
            else:
                return f"{size // (1024 * 1024)} MB"
        return ""
    
    def get_video_embed_url(self):
        """Convertit les URLs YouTube/Vimeo en URLs d'intégration"""
        if not self.video_url:
            return ""
            
        url = self.video_url
        
        # YouTube
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        
        # Vimeo
        elif 'vimeo.com/' in url:
            video_id = url.split('vimeo.com/')[1].split('?')[0]
            return f"https://player.vimeo.com/video/{video_id}"
        
        return url
    
    def has_media(self):
        """Vérifie si le bloc a du contenu média"""
        return bool(self.image or self.document or self.video_file or self.video_url or self.video_embed_code)