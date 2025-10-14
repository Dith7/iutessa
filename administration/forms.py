from django import forms
from django.core.validators import FileExtensionValidator
from pages.models import Course


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


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'code', 'description', 'filiere', 
            'duration', 'level', 'instructor', 'credits', 
            'is_required', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Titre du cours'
            }),
            'code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Ex: BTS101'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 5,
                'placeholder': 'Description détaillée du cours'
            }),
            'filiere': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Ex: 30 heures, 1 semestre'
            }),
            'level': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Ex: Débutant, Intermédiaire, Avancé'
            }),
            'instructor': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Nom de l\'instructeur'
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '0',
                'min': '0'
            }),
            'is_required': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': 'Titre du cours',
            'code': 'Code',
            'description': 'Description',
            'filiere': 'Filière',
            'duration': 'Durée',
            'level': 'Niveau',
            'instructor': 'Instructeur',
            'credits': 'Crédits',
            'is_required': 'Cours obligatoire',
            'image': 'Image',
        }

