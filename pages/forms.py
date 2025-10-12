from django import forms
from django.core.validators import FileExtensionValidator
from .models import Post, PostImage, PostDocument, Comment

# ============================================
# POST FORMS
# ============================================

class PostForm(forms.ModelForm):
    """Formulaire principal pour créer/éditer un article"""
    
    class Meta:
        model = Post
        fields = [
            'title', 'featured_image', 'excerpt', 'content',
            'category', 'tags', 'video_url', 'video_file', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'placeholder': 'Titre de l\'article'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'rows': 3,
                'placeholder': 'Résumé court (300 caractères max)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'rows': 15,
                'placeholder': 'Contenu de l\'article...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'placeholder': 'Innovation, Recherche, Technologie (séparer par des virgules)'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'placeholder': 'https://www.youtube.com/watch?v=... ou https://vimeo.com/...'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'accept': 'video/*'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none'
            }),
        }
    
    def clean_featured_image(self):
        """Valider l'image à la une"""
        image = self.cleaned_data.get('featured_image')
        if image:
            # Vérifier la taille (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('L\'image ne doit pas dépasser 5MB')
            # Vérifier l'extension
            allowed = ['jpg', 'jpeg', 'png', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in allowed:
                raise forms.ValidationError(f'Format non autorisé. Utilisez: {", ".join(allowed)}')
        return image
    
    def clean_video_file(self):
        """Valider le fichier vidéo"""
        video = self.cleaned_data.get('video_file')
        if video:
            # Vérifier la taille (max 50MB)
            if video.size > 50 * 1024 * 1024:
                raise forms.ValidationError('La vidéo ne doit pas dépasser 50MB')
            # Vérifier l'extension
            allowed = ['mp4', 'webm', 'avi', 'mov']
            ext = video.name.split('.')[-1].lower()
            if ext not in allowed:
                raise forms.ValidationError(f'Format non autorisé. Utilisez: {", ".join(allowed)}')
        return video
    
    def clean(self):
        """Validation globale"""
        cleaned_data = super().clean()
        video_url = cleaned_data.get('video_url')
        video_file = cleaned_data.get('video_file')
        
        # Ne pas avoir les deux en même temps
        if video_url and video_file:
            raise forms.ValidationError('Choisissez soit une URL vidéo, soit un fichier vidéo, pas les deux.')
        
        return cleaned_data


class PostImageForm(forms.ModelForm):
    """Formulaire pour ajouter des images à la galerie"""
    
    class Meta:
        model = PostImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'placeholder': 'Légende de l\'image (optionnel)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-20 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'min': 0
            }),
        }
    
    def clean_image(self):
        """Valider l'image"""
        image = self.cleaned_data.get('image')
        if image:
            # Taille max 5MB
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('L\'image ne doit pas dépasser 5MB')
            # Extensions autorisées
            allowed = ['jpg', 'jpeg', 'png', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in allowed:
                raise forms.ValidationError(f'Format non autorisé. Utilisez: {", ".join(allowed)}')
        return image


class PostDocumentForm(forms.ModelForm):
    """Formulaire pour joindre des documents PDF"""
    
    class Meta:
        model = PostDocument
        fields = ['title', 'file', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'placeholder': 'Titre du document'
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'accept': '.pdf,.doc,.docx'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'rows': 3,
                'placeholder': 'Description du document (optionnel)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-20 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'min': 0
            }),
        }
    
    def clean_file(self):
        """Valider le fichier"""
        file = self.cleaned_data.get('file')
        if file:
            # Taille max 10MB
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Le document ne doit pas dépasser 10MB')
            # Extensions autorisées
            allowed = ['pdf', 'doc', 'docx']
            ext = file.name.split('.')[-1].lower()
            if ext not in allowed:
                raise forms.ValidationError(f'Format non autorisé. Utilisez: {", ".join(allowed)}')
        return file


class CommentForm(forms.ModelForm):
    """Formulaire pour les commentaires"""
    
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'placeholder': 'Votre nom'
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'placeholder': 'Votre email'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
                'rows': 4,
                'placeholder': 'Votre commentaire...'
            }),
        }
    
    def clean_content(self):
        """Valider le contenu du commentaire"""
        content = self.cleaned_data.get('content')
        if content and len(content) < 10:
            raise forms.ValidationError('Le commentaire doit contenir au moins 10 caractères')
        return content


# ============================================
# FORMSETS
# ============================================

from django.forms import inlineformset_factory

# Formset pour gérer plusieurs images en même temps
PostImageFormSet = inlineformset_factory(
    Post,
    PostImage,
    form=PostImageForm,
    extra=3,  # Nombre de formulaires vides à afficher
    can_delete=True
)

# Formset pour gérer plusieurs documents en même temps
PostDocumentFormSet = inlineformset_factory(
    Post,
    PostDocument,
    form=PostDocumentForm,
    extra=2,
    can_delete=True
)


# ============================================
# FILTRES
# ============================================

class PostFilterForm(forms.Form):
    """Formulaire de recherche/filtrage pour le blog"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none',
            'placeholder': 'Rechercher un article...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=None,  # Sera défini dans __init__
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#3db166] focus:outline-none'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.filter(posts__status='published').distinct()