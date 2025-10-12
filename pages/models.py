from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
import os

User = get_user_model()

# ============================================
# BLOG
# ============================================

class Category(models.Model):
    """Catégories pour blog et portfolio"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """Articles de blog avec support multimédia"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    ]
    
    # Contenu principal
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Auteur")
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True, null=True, verbose_name="Image à la une")
    excerpt = models.TextField(max_length=300, verbose_name="Extrait")
    content = models.TextField(verbose_name="Contenu")
    
    # Classification
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name="Catégorie")
    tags = models.CharField(max_length=200, blank=True, help_text="Séparer par des virgules", verbose_name="Tags")
    
    # Vidéo (optionnelle)
    video_url = models.URLField(blank=True, verbose_name="URL Vidéo (YouTube/Vimeo)", help_text="Lien YouTube ou Vimeo")
    video_file = models.FileField(upload_to='blog/videos/', blank=True, null=True, verbose_name="Ou fichier vidéo")
    
    # Statut et stats
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Publié le")
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['slug']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('pages:blog_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        """Retourne les tags sous forme de liste"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_video_embed_url(self):
        """Retourne l'URL embed pour YouTube/Vimeo"""
        if not self.video_url:
            return None
        
        url = self.video_url
        
        # YouTube
        if 'youtube.com' in url or 'youtu.be' in url:
            if 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[-1].split('?')[0]
            else:
                video_id = url.split('v=')[-1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        
        # Vimeo
        elif 'vimeo.com' in url:
            video_id = url.split('vimeo.com/')[-1].split('?')[0]
            return f"https://player.vimeo.com/video/{video_id}"
        
        return None


class PostImage(models.Model):
    """Images supplémentaires pour un article (galerie)"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name="Article")
    image = models.ImageField(upload_to='blog/gallery/', verbose_name="Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Légende")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"Image {self.id} - {self.post.title}"


class PostDocument(models.Model):
    """Documents PDF joints à un article"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='documents', verbose_name="Article")
    file = models.FileField(upload_to='blog/documents/', verbose_name="Fichier PDF")
    title = models.CharField(max_length=200, verbose_name="Titre du document")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploadé le")
    
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.title
    
    def get_file_size(self):
        """Retourne la taille du fichier en format lisible"""
        if self.file:
            size = self.file.size
            for unit in ['o', 'Ko', 'Mo', 'Go']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 o"
    
    def get_file_extension(self):
        """Retourne l'extension du fichier"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ""


class Comment(models.Model):
    """Commentaires sur les articles"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Article")
    author_name = models.CharField(max_length=100, verbose_name="Nom")
    author_email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Commentaire")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commentaire de {self.author_name} sur {self.post.title}"


# ============================================
# PORTFOLIO
# ============================================

class Project(models.Model):
    """Projets du portfolio"""
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    featured_image = models.ImageField(upload_to='portfolio/images/', verbose_name="Image principale")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects', verbose_name="Catégorie")
    client = models.CharField(max_length=100, blank=True, verbose_name="Client")
    date_completed = models.DateField(null=True, blank=True, verbose_name="Date de réalisation")
    project_url = models.URLField(blank=True, verbose_name="URL du projet")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['order', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('pages:portfolio_detail', kwargs={'slug': self.slug})


# ============================================
# EVENTS
# ============================================

class Event(models.Model):
    """Événements et calendrier"""
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    location = models.CharField(max_length=200, verbose_name="Lieu")
    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Image")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-start_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# ============================================
# COURSES
# ============================================

class Course(models.Model):
    """Cours et formations"""
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    duration = models.CharField(max_length=50, verbose_name="Durée")
    level = models.CharField(max_length=50, verbose_name="Niveau")
    instructor = models.CharField(max_length=100, verbose_name="Instructeur")
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name="Image")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['title']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title