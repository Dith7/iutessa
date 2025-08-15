from django import forms
from django.core.validators import FileExtensionValidator
from pages.models import PageBlock


class PageBlockForm(forms.ModelForm):
    """Formulaire pour créer/modifier un bloc"""
    
    class Meta:
        model = PageBlock
        fields = [
            'title', 'subtitle', 'content', 'block_type', 'order', 'status',
            'image', 'document', 'document_title', 
            'video_type', 'video_file', 'video_url', 'video_embed_code', 'video_thumbnail',
            'link_url', 'link_text'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Titre du bloc'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Sous-titre (optionnel)'
            }),
            'block_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-24 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'min': '0'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'document': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.rtf'
            }),
            'document_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Titre du document'
            }),
            'video_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'video/*'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'https://www.youtube.com/watch?v=...'
            }),
            'video_embed_code': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4,
                'placeholder': '<iframe src="..."></iframe>'
            }),
            'video_thumbnail': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'link_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'https://...'
            }),
            'link_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Texte du lien'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ajouter des classes CSS selon le type de champ
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] += ' cursor-pointer'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] += ' file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'

    def clean(self):
        cleaned_data = super().clean()
        video_type = cleaned_data.get('video_type')
        video_file = cleaned_data.get('video_file')
        video_url = cleaned_data.get('video_url')
        video_embed_code = cleaned_data.get('video_embed_code')

        # Validation vidéo selon le type
        if video_type == 'local' and not video_file:
            self.add_error('video_file', 'Fichier vidéo requis pour le type "local".')
        elif video_type in ['youtube', 'vimeo'] and not video_url:
            self.add_error('video_url', 'URL requise pour YouTube/Vimeo.')
        elif video_type == 'embed' and not video_embed_code:
            self.add_error('video_embed_code', 'Code d\'intégration requis.')

        return cleaned_data



class MultipleFileInput(forms.ClearableFileInput):
    """Widget pour permettre l'upload de plusieurs fichiers."""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Champ pour gérer plusieurs fichiers dans un seul input."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """Nettoie et retourne une liste de fichiers."""
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(f, initial) for f in data]
        return [single_file_clean(data, initial)]


class MediaUploadForm(forms.Form):
    media_type = forms.ChoiceField(
        choices=[
            ('image', 'Image'),
            ('document', 'Document'),
            ('video', 'Vidéo')
        ],
        required=True
    )

    file = MultipleFileField(
        required=True,
        widget=MultipleFileInput(attrs={
            'class': 'hidden',
            'id': 'media-upload-input',
            'multiple': True
        })
    )

    def clean_file(self):
        files = self.cleaned_data.get('file') or []
        media_type = self.cleaned_data.get('media_type')

        allowed_extensions = {
            'image': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
            'document': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf'],
            'video': ['mp4', 'webm', 'avi', 'mov']
        }

        for f in files:
            # Taille max : 50 Mo
            if f.size > 50 * 1024 * 1024:
                raise forms.ValidationError(
                    f'Le fichier "{f.name}" est trop volumineux (max 50MB).'
                )

            # Vérification de l'extension
            if media_type in allowed_extensions:
                ext = f.name.split('.')[-1].lower()
                if ext not in allowed_extensions[media_type]:
                    raise forms.ValidationError(
                        f'Le fichier "{f.name}" a une extension non autorisée pour {media_type}. '
                        f'Extensions autorisées : {", ".join(allowed_extensions[media_type])}'
                    )

        return files



class BlockFilterForm(forms.Form):
    """Formulaire de filtres pour la liste des blocs"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Rechercher par titre, contenu...'
        })
    )
    
    block_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les types')] + PageBlock.BLOCK_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les statuts')] + PageBlock.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )
    
    SORT_CHOICES = [
        ('-updated_at', 'Plus récents'),
        ('updated_at', 'Plus anciens'),
        ('title', 'Titre A-Z'),
        ('-title', 'Titre Z-A'),
        ('order', 'Ordre croissant'),
        ('-order', 'Ordre décroissant'),
    ]
    
    sort = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        initial='-updated_at',
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )