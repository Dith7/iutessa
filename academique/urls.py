# academique/urls.py - Ajouter cette URL après admin_validate_document

from django.urls import path
from . import views

app_name = 'academique'

urlpatterns = [
    # =================== URLs ADMIN ===================
    # Gestion des filières
    path('administration/filieres/', 
         views.admin_filieres_list, 
         name='admin_filieres_list'),
    
    path('administration/filieres/nouvelle/', 
         views.admin_filiere_create, 
         name='admin_filiere_create'),
    
    path('administration/filieres/<int:pk>/modifier/', 
         views.admin_filiere_edit, 
         name='admin_filiere_edit'),
    
    # Gestion des étudiants
    path('administration/etudiants/', 
         views.admin_etudiants_list, 
         name='admin_etudiants_list'),
    
    path('administration/etudiants/import/', 
         views.admin_import_etudiants, 
         name='admin_import_etudiants'),
    
    path('administration/etudiants/export/', 
         views.export_etudiants_excel, 
         name='export_etudiants_excel'),
    
    # Validation des documents
    path('administration/documents/', 
         views.admin_documents_validation, 
         name='admin_documents_validation'),
    
    path('administration/documents/<int:doc_id>/valider/', 
         views.admin_validate_document, 
         name='admin_validate_document'),
    
    # NOUVELLE URL: Validation inscription
    path('administration/etudiants/<int:etudiant_id>/valider/', 
         views.admin_validate_inscription, 
         name='admin_validate_inscription'),
    
    # =================== URLs ÉTUDIANT ===================
    # Inscription et profil
    path('inscription/', 
         views.etudiant_inscription, 
         name='etudiant_inscription'),
    
    path('profil/', 
         views.etudiant_profile, 
         name='etudiant_profile'),
    
    # Gestion des documents
    path('documents/', 
         views.etudiant_documents, 
         name='etudiant_documents'),
    
    path('documents/<int:doc_id>/supprimer/', 
         views.ajax_delete_document, 
         name='ajax_delete_document'),
    
    # Téléchargement de la fiche
    path('fiche-inscription.pdf', 
         views.etudiant_fiche_pdf, 
         name='etudiant_fiche_pdf'),
    
    # =================== URLs PUBLIQUES ===================
    # Liste des filières
    path('filieres/', 
         views.filieres_list_public, 
         name='filieres_list_public'),
    
    path('filieres/<str:code>/', 
         views.filiere_detail_public, 
         name='filiere_detail_public'),
    
    # =================== URLs AJAX ===================
    # Statistiques dashboard
    path('ajax/stats/', 
         views.ajax_stats_dashboard, 
         name='ajax_stats_dashboard'),
]