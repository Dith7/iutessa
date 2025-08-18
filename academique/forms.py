# academique/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Filiere, EtudiantAcademique, DocumentEtudiant, ImportEtudiant

User = get_user_model()

class FiliereForm(forms.ModelForm):
    """Formulaire pour créer/modifier une filière"""
    
    class Meta:
        model = Filiere
        fields = [
            'nom', 'code', 'description', 'places_disponibles',
            'diplome_requis', 'domaine_requis', 'frais_inscription',
            'duree_formation', 'statut'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la filière'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code unique (ex: GI, GM...)',
                'maxlength': 10
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description de la filière...'
            }),
            'places_disponibles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 200
            }),
            'diplome_requis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'domaine_requis': forms.Select(attrs={
                'class': 'form-control'
            }),
            'frais_inscription': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000'
            }),
            'duree_formation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex: 3 ans'
            }),
            'statut': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_code(self):
        code = self.cleaned_data['code'].upper()
        # Vérifier l'unicité du code
        if self.instance.pk:
            if Filiere.objects.exclude(pk=self.instance.pk).filter(code=code).exists():
                raise ValidationError('Ce code existe déjà.')
        else:
            if Filiere.objects.filter(code=code).exists():
                raise ValidationError('Ce code existe déjà.')
        return code


class EtudiantInscriptionForm(forms.ModelForm):
    """Formulaire d'inscription pour les étudiants"""
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.filter(statut='active').order_by('nom'),
        label="Filière d'inscription",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    adresse = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Adresse complète...'
        })
    )
    
    class Meta:
        model = EtudiantAcademique
        fields = [ 
            'filiere',
            'nom', 'prenoms', 'date_naissance', 'lieu_naissance',
            'nationalite', 'region_origine', 'cni', 'telephone',
            'email_personnel', 'adresse', 'nom_pere', 'telephone_pere',
            'nom_mere', 'telephone_mere', 'diplome_obtenu', 'annee_obtention'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'prenoms': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            
            'lieu_naissance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville, Pays'
            }),
            'nationalite': forms.Select(attrs={
                'class': 'form-control'
            }),
            'region_origine': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Région d\'origine'
            }),
            'cni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro CNI'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+237 6XX XXX XXX'
            }),
            'email_personnel': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@exemple.com'
            }),
            'nom_pere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom complet du père'
            }),
            'telephone_pere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+237 6XX XXX XXX'
            }),
            'nom_mere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom complet de la mère'
            }),
            'telephone_mere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+237 6XX XXX XXX'
            }),
            'diplome_obtenu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Baccalauréat série...'
            }),
            'annee_obtention': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2010,
                'max': 2025
            })
        }
    
    def clean_cni(self):
        cni = self.cleaned_data['cni']
        # Vérifier l'unicité de la CNI
        if self.instance.pk:
            if EtudiantAcademique.objects.exclude(pk=self.instance.pk).filter(cni=cni).exists():
                raise ValidationError('Cette CNI est déjà utilisée.')
        else:
            if EtudiantAcademique.objects.filter(cni=cni).exists():
                raise ValidationError('Cette CNI est déjà utilisée.')
        return cni
    
    def clean_email_personnel(self):
        email = self.cleaned_data['email_personnel']
        # Vérifier l'unicité de l'email
        if self.instance.pk:
            if EtudiantAcademique.objects.exclude(pk=self.instance.pk).filter(email_personnel=email).exists():
                raise ValidationError('Cet email est déjà utilisé.')
        else:
            if EtudiantAcademique.objects.filter(email_personnel=email).exists():
                raise ValidationError('Cet email est déjà utilisé.')
        return email


class DocumentUploadForm(forms.ModelForm):
    """Formulaire d'upload de documents"""
    
    class Meta:
        model = DocumentEtudiant
        fields = ['type_document', 'fichier']
        widgets = {
            'type_document': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fichier': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }
    
    def clean_fichier(self):
        fichier = self.cleaned_data['fichier']
        
        # Vérifier la taille (max 5MB)
        if fichier.size > 5 * 1024 * 1024:
            raise ValidationError('Le fichier ne doit pas dépasser 5MB.')
        
        # Vérifier le type de fichier
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
        if fichier.content_type not in allowed_types:
            raise ValidationError('Seuls les fichiers PDF, JPG et PNG sont autorisés.')
        
        return fichier


class ImportEtudiantForm(forms.ModelForm):
    """Formulaire d'import Excel des étudiants"""
    
    class Meta:
        model = ImportEtudiant
        fields = ['fichier']
        widgets = {
            'fichier': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.xlsx,.xls',
                'required': True
            })
        }
    
    def clean_fichier(self):
        fichier = self.cleaned_data['fichier']
        
        # Vérifier la taille (max 10MB)
        if fichier.size > 10 * 1024 * 1024:
            raise ValidationError('Le fichier ne doit pas dépasser 10MB.')
        
        # Vérifier l'extension
        if not fichier.name.endswith(('.xlsx', '.xls')):
            raise ValidationError('Seuls les fichiers Excel (.xlsx, .xls) sont autorisés.')
        
        return fichier


class FiltreEtudiantForm(forms.Form):
    """Formulaire de filtrage des étudiants"""
    
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(),
        required=False,
        empty_label="Toutes les filières",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    statut_inscription = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + EtudiantAcademique.STATUT_INSCRIPTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    statut_validation = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + EtudiantAcademique.STATUT_VALIDATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    recherche = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par nom, matricule, CNI...'
        })
    )


class ValidationDocumentForm(forms.ModelForm):
    """Formulaire de validation de document"""
    
    class Meta:
        model = DocumentEtudiant
        fields = ['valide', 'commentaire']
        widgets = {
            'valide': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaire optionnel...'
            })
        }


class RechercheEtudiantForm(forms.Form):
    """Formulaire de recherche rapide d'étudiant"""
    
    terme = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom, matricule, CNI...',
            'autocomplete': 'off'
        })
    )


class StatistiquesForm(forms.Form):
    """Formulaire pour les filtres de statistiques"""
    
    PERIODE_CHOICES = [
        ('semaine', 'Cette semaine'),
        ('mois', 'Ce mois'),
        ('trimestre', 'Ce trimestre'),
        ('annee', 'Cette année'),
        ('tout', 'Toute la période')
    ]
    
    periode = forms.ChoiceField(
        choices=PERIODE_CHOICES,
        initial='mois',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(),
        required=False,
        empty_label="Toutes les filières",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ExportForm(forms.Form):
    """Formulaire pour les exports"""
    
    FORMAT_CHOICES = [
        ('excel', 'Excel (.xlsx)'),
        ('pdf', 'PDF'),
        ('csv', 'CSV')
    ]
    
    format_export = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        initial='excel',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    inclure_documents = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    filtres = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )