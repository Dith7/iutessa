# academique/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Filiere, EtudiantAcademique, DocumentEtudiant, ImportEtudiant

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'nom', 'domaine_requis', 
        'places_occupation', 'taux_occupation_display', 'statut'
    ]
    list_filter = ['domaine_requis', 'statut', 'created_at']
    search_fields = ['nom', 'code', 'description']
    list_editable = ['statut']
    ordering = ['code']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'code', 'description', 'statut')
        }),
        ('Admission', {
            'fields': ('places_disponibles', 'diplome_requis', 'domaine_requis')
        }),
        ('Formation', {
            'fields': ('duree_formation', 'frais_inscription')
        }),
    )
    
    def places_occupation(self, obj):
        return f"{obj.places_occupees}/{obj.places_disponibles}"
    places_occupation.short_description = "Places"
    
    def taux_occupation_display(self, obj):
        taux = obj.taux_occupation
        color = 'red' if taux > 90 else 'orange' if taux > 75 else 'green'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, taux
        )
    taux_occupation_display.short_description = "Taux occupation"


class DocumentEtudiantInline(admin.TabularInline):
    model = DocumentEtudiant
    extra = 0
    readonly_fields = ['date_upload', 'valide_par']
    fields = ['type_document', 'fichier', 'valide', 'commentaire', 'date_upload']


@admin.register(EtudiantAcademique)
class EtudiantAcademiqueAdmin(admin.ModelAdmin):
    list_display = [
        'numero_matricule', 'nom_complet', 'filiere', 
        'statut_inscription', 'statut_validation', 'documents_status'
    ]
    list_filter = [
        'statut_inscription', 'statut_validation', 'filiere',
        'nationalite', 'date_inscription'
    ]
    search_fields = [
        'nom', 'prenoms', 'numero_matricule', 'cni', 
        'email_personnel', 'telephone'
    ]
    list_editable = ['statut_validation']
    date_hierarchy = 'date_inscription'
    inlines = [DocumentEtudiantInline]
    
    fieldsets = (
        ('Informations système', {
            'fields': ('user', 'filiere', 'numero_matricule', 'statut_inscription', 'statut_validation')
        }),
        ('Identité', {
            'fields': ('nom', 'prenoms', 'date_naissance', 'lieu_naissance', 'nationalite', 'region_origine', 'cni')
        }),
        ('Contact', {
            'fields': ('telephone', 'email_personnel', 'adresse')
        }),
        ('Parents/Tuteurs', {
            'fields': ('nom_pere', 'telephone_pere', 'nom_mere', 'telephone_mere')
        }),
        ('Formation', {
            'fields': ('diplome_obtenu', 'annee_obtention')
        }),
    )
    
    readonly_fields = ['numero_matricule', 'date_inscription', 'date_validation']
    
    def nom_complet(self, obj):
        return obj.nom_complet
    nom_complet.short_description = "Nom complet"
    
    def documents_status(self, obj):
        total_docs = obj.documents.count()
        docs_valides = obj.documents.filter(valide=True).count()
        
        if total_docs == 0:
            return format_html('<span style="color: red;">Aucun document</span>')
        
        percentage = (docs_valides / total_docs) * 100
        color = 'green' if percentage == 100 else 'orange' if percentage > 50 else 'red'
        
        return format_html(
            '<span style="color: {};">{}/{} ({:.0f}%)</span>',
            color, docs_valides, total_docs, percentage
        )
    documents_status.short_description = "Documents"
    
    actions = ['valider_etudiants', 'rejeter_etudiants', 'exporter_excel']
    
    def valider_etudiants(self, request, queryset):
        updated = queryset.update(
            statut_validation='valide',
            date_validation=timezone.now()
        )
        self.message_user(request, f'{updated} étudiant(s) validé(s).')
    valider_etudiants.short_description = "Valider les étudiants sélectionnés"
    
    def rejeter_etudiants(self, request, queryset):
        updated = queryset.update(statut_validation='rejete')
        self.message_user(request, f'{updated} étudiant(s) rejeté(s).')
    rejeter_etudiants.short_description = "Rejeter les étudiants sélectionnés"


@admin.register(DocumentEtudiant)
class DocumentEtudiantAdmin(admin.ModelAdmin):
    list_display = [
        'etudiant', 'type_document', 'valide', 
        'date_upload', 'valide_par'
    ]
    list_filter = ['type_document', 'valide', 'date_upload']
    search_fields = ['etudiant__nom', 'etudiant__prenoms', 'etudiant__numero_matricule']
    list_editable = ['valide']
    date_hierarchy = 'date_upload'
    
    readonly_fields = ['date_upload', 'etudiant_info']
    
    def etudiant_info(self, obj):
        return format_html(
            '<strong>{}</strong><br>Matricule: {}<br>Filière: {}',
            obj.etudiant.nom_complet,
            obj.etudiant.numero_matricule,
            obj.etudiant.filiere
        )
    etudiant_info.short_description = "Informations étudiant"
    
    actions = ['valider_documents', 'invalider_documents']
    
    def valider_documents(self, request, queryset):
        updated = queryset.update(valide=True, valide_par=request.user)
        self.message_user(request, f'{updated} document(s) validé(s).')
    valider_documents.short_description = "Valider les documents sélectionnés"
    
    def invalider_documents(self, request, queryset):
        updated = queryset.update(valide=False, valide_par=None)
        self.message_user(request, f'{updated} document(s) invalidé(s).')
    invalider_documents.short_description = "Invalider les documents sélectionnés"


@admin.register(ImportEtudiant)
class ImportEtudiantAdmin(admin.ModelAdmin):
    list_display = [
        'date_import', 'importe_par', 'nombre_total', 
        'nombre_succes', 'nombre_erreurs', 'taux_succes'
    ]
    list_filter = ['date_import', 'importe_par']
    readonly_fields = [
        'date_import', 'nombre_total', 'nombre_succes', 
        'nombre_erreurs', 'rapport_erreurs'
    ]
    
    def taux_succes(self, obj):
        if obj.nombre_total == 0:
            return "0%"
        taux = (obj.nombre_succes / obj.nombre_total) * 100
        color = 'green' if taux == 100 else 'orange' if taux > 80 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, taux
        )
    taux_succes.short_description = "Taux de succès"
    
    def has_add_permission(self, request):
        return False  # Import se fait via interface dédiée