# pages/events_forms.py
# Fichier séparé pour le formulaire Event

from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    """Formulaire de création et modification d'événements"""
    
    class Meta:
        model = Event
        fields = [
            'title', 
            'description', 
            'start_date', 
            'end_date',
            'location', 
            'image', 
            'is_featured'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Titre de l\'événement'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 5,
                'placeholder': 'Description complète de l\'événement'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'datetime-local'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Lieu de l\'événement (ex: Campus IUTESSA)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }
        
        labels = {
            'title': 'Titre de l\'événement',
            'description': 'Description',
            'start_date': 'Date et heure de début',
            'end_date': 'Date et heure de fin',
            'location': 'Lieu',
            'image': 'Image de l\'événement',
            'is_featured': 'Événement vedette',
        }
        
        help_texts = {
            'is_featured': 'L\'événement sera mis en avant sur la page d\'accueil',
            'location': 'Laissez vide pour "Campus IUTESSA" par défaut',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError(
                    "La date de fin doit être après la date de début."
                )
        
        return cleaned_data