# academique/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid

User = get_user_model()

class Filiere(models.Model):
    DOMAINE_CHOICES = [
        ('general', 'Général'),
        ('scientifique', 'Scientifique'),
        ('technique', 'Technique Industrielle'),
        ('tous', 'Tous domaines confondus')
    ]
    
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspendue', 'Suspendue')
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom de la filière")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    description = models.TextField(blank=True, verbose_name="Description")
    places_disponibles = models.PositiveIntegerField(default=60, verbose_name="Places disponibles")
    places_occupees = models.PositiveIntegerField(default=0, verbose_name="Places occupées")
    
    diplome_requis = models.CharField(
        max_length=200, 
        default="Diplôme de fin d'étude du second cycle",
        verbose_name="Diplôme requis"
    )
    domaine_requis = models.CharField(
        max_length=20, 
        choices=DOMAINE_CHOICES,
        default='tous',
        verbose_name="Domaine requis"
    )
    
    frais_inscription = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=15000,
        verbose_name="Frais d'inscription (FCFA)"
    )
    duree_formation = models.CharField(
        max_length=50, 
        default="3 ans",
        verbose_name="Durée de formation"
    )
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES,
        default='active',
        verbose_name="Statut"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.code} - {self.nom}"
    
    @property
    def places_restantes(self):
        return self.places_disponibles - self.places_occupees
    
    @property
    def taux_occupation(self):
        if self.places_disponibles == 0:
            return 0
        return (self.places_occupees / self.places_disponibles) * 100


class EtudiantAcademique(models.Model):
    STATUT_INSCRIPTION_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé')
    ]
    
    STATUT_VALIDATION_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté')
    ]
    
    NATIONALITE_CHOICES = [
        ('camerounaise', 'Camerounaise'),
        ('autre', 'Autre')
    ]
    
    # Relations
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='etudiant_academique')
    filiere = models.ForeignKey(Filiere, on_delete=models.PROTECT, related_name='etudiants')
    
    # Informations personnelles
    nom = models.CharField(max_length=50, verbose_name="Nom")
    prenoms = models.CharField(max_length=100, verbose_name="Prénoms")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    nationalite = models.CharField(
        max_length=20, 
        choices=NATIONALITE_CHOICES,
        default='camerounaise',
        verbose_name="Nationalité"
    )
    region_origine = models.CharField(max_length=50, verbose_name="Région d'origine")
    
    # Documents d'identité
    cni = models.CharField(
        max_length=50, 
        unique=True,
        validators=[RegexValidator(r'^[0-9A-Z]+$', 'Format CNI invalide')],
        verbose_name="Numéro CNI"
    )
    
    # Contact
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?[0-9\s\-\(\)]+$', 'Numéro de téléphone invalide')],
        verbose_name="Téléphone"
    )
    email_personnel = models.EmailField(verbose_name="Email personnel")
    adresse = models.TextField(verbose_name="Adresse")
    
    # Parents/Tuteurs
    nom_pere = models.CharField(max_length=100, verbose_name="Nom du père")
    telephone_pere = models.CharField(
        max_length=15, 
        blank=True,
        validators=[RegexValidator(r'^\+?[0-9\s\-\(\)]+$', 'Numéro invalide')],
        verbose_name="Téléphone père"
    )
    nom_mere = models.CharField(max_length=100, verbose_name="Nom de la mère")
    telephone_mere = models.CharField(
        max_length=15, 
        blank=True,
        validators=[RegexValidator(r'^\+?[0-9\s\-\(\)]+$', 'Numéro invalide')],
        verbose_name="Téléphone mère"
    )
    
    # Formation
    diplome_obtenu = models.CharField(max_length=100, verbose_name="Diplôme obtenu")
    annee_obtention = models.PositiveIntegerField(verbose_name="Année d'obtention")
    
    # Système
    numero_matricule = models.CharField(
        max_length=20, 
        unique=True, 
        blank=True,
        verbose_name="Numéro matricule"
    )
    statut_inscription = models.CharField(
        max_length=20,
        choices=STATUT_INSCRIPTION_CHOICES,
        default='en_attente',
        verbose_name="Statut inscription"
    )
    statut_validation = models.CharField(
        max_length=20,
        choices=STATUT_VALIDATION_CHOICES,
        default='en_attente',
        verbose_name="Statut validation"
    )
    
    # Dates
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    
    class Meta:
        verbose_name = "Étudiant Académique"
        verbose_name_plural = "Étudiants Académiques"
        ordering = ['-date_inscription']
    
    def __str__(self):
        return f"{self.numero_matricule} - {self.nom} {self.prenoms}"
    
    def save(self, *args, **kwargs):
        if not self.numero_matricule:
            self.numero_matricule = self.generer_matricule()
        super().save(*args, **kwargs)
    
    def generer_matricule(self):
        """Génère un matricule unique format: IUTESSA-YYYY-XXXX"""
        annee = timezone.now().year
        # Compte les étudiants de l'année
        count = EtudiantAcademique.objects.filter(
            date_inscription__year=annee
        ).count() + 1
        return f"IUTESSA-{annee}-{count:04d}"
    
    @property
    def nom_complet(self):
        return f"{self.nom} {self.prenoms}"


class DocumentEtudiant(models.Model):
    TYPE_DOCUMENT_CHOICES = [
        ('acte_naissance', 'Acte de naissance'),
        ('diplome', 'Diplôme du Baccalauréat'),
        ('releve_notes', 'Relevé de notes'),
        ('certificat_medical', 'Certificat médical'),
        ('photo', 'Photo 4x4'),
        ('recu_paiement', 'Reçu de paiement'),
        ('lettre_motivation', 'Lettre de motivation')
    ]
    
    etudiant = models.ForeignKey(
        EtudiantAcademique, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    type_document = models.CharField(
        max_length=20, 
        choices=TYPE_DOCUMENT_CHOICES,
        verbose_name="Type de document"
    )
    fichier = models.FileField(
        upload_to='documents/etudiants/%Y/%m/',
        verbose_name="Fichier"
    )
    date_upload = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")
    valide = models.BooleanField(default=False, verbose_name="Validé")
    valide_par = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='documents_valides',
        verbose_name="Validé par"
    )
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    class Meta:
        verbose_name = "Document Étudiant"
        verbose_name_plural = "Documents Étudiants"
        unique_together = ['etudiant', 'type_document']
        ordering = ['-date_upload']
    
    def __str__(self):
        return f"{self.etudiant.nom_complet} - {self.get_type_document_display()}"


class ImportEtudiant(models.Model):
    """Modèle pour tracer les imports d'étudiants"""
    fichier = models.FileField(
        upload_to='imports/etudiants/%Y/%m/',
        verbose_name="Fichier Excel"
    )
    date_import = models.DateTimeField(auto_now_add=True)
    importe_par = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_total = models.PositiveIntegerField(default=0)
    nombre_succes = models.PositiveIntegerField(default=0)
    nombre_erreurs = models.PositiveIntegerField(default=0)
    rapport_erreurs = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Import Étudiant"
        verbose_name_plural = "Imports Étudiants"
        ordering = ['-date_import']
    
    def __str__(self):
        return f"Import {self.date_import.strftime('%d/%m/%Y %H:%M')} - {self.nombre_succes}/{self.nombre_total}"