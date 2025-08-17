# academique/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.decorators import role_required, admin_required
from .models import Filiere, EtudiantAcademique, DocumentEtudiant, ImportEtudiant
from .forms import (
    FiliereForm, EtudiantInscriptionForm, DocumentUploadForm, 
    ImportEtudiantForm, FiltreEtudiantForm, ValidationDocumentForm
)
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import openpyxl

User = get_user_model()

# =================== VIEWS ADMIN ===================

@admin_required
def admin_filieres_list(request):
    """Liste des filières pour l'admin"""
    filieres = Filiere.objects.all().order_by('nom')
    
    # Filtrage
    search = request.GET.get('search', '')
    if search:
        filieres = filieres.filter(
            Q(nom__icontains=search) | 
            Q(code__icontains=search) |
            Q(description__icontains=search)
        )
    
    paginator = Paginator(filieres, 10)
    page = request.GET.get('page')
    filieres = paginator.get_page(page)
    
    context = {
        'filieres': filieres,
        'search': search,
        'total_filieres': Filiere.objects.count(),
        'active_filieres': Filiere.objects.filter(statut='active').count(),
    }
    
    return render(request, 'academique/admin/filieres_list.html', context)


@admin_required
def admin_filiere_create(request):
    """Création d'une nouvelle filière"""
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            filiere = form.save()
            messages.success(request, f'Filière "{filiere.nom}" créée avec succès.')
            return redirect('academique:admin_filieres_list')
    else:
        form = FiliereForm()
    
    return render(request, 'academique/admin/filiere_form.html', {
        'form': form,
        'title': 'Créer une filière',
        'action': 'create'
    })


@admin_required
def admin_filiere_edit(request, pk):
    """Modification d'une filière"""
    filiere = get_object_or_404(Filiere, pk=pk)
    
    if request.method == 'POST':
        form = FiliereForm(request.POST, instance=filiere)
        if form.is_valid():
            form.save()
            messages.success(request, f'Filière "{filiere.nom}" modifiée avec succès.')
            return redirect('academique:admin_filieres_list')
    else:
        form = FiliereForm(instance=filiere)
    
    return render(request, 'academique/admin/filiere_form.html', {
        'form': form,
        'filiere': filiere,
        'title': f'Modifier {filiere.nom}',
        'action': 'edit'
    })


@admin_required
def admin_etudiants_list(request):
    """Liste des étudiants pour l'admin"""
    etudiants = EtudiantAcademique.objects.select_related('user', 'filiere').all()
    
    # Filtrage
    form = FiltreEtudiantForm(request.GET)
    if form.is_valid():
        filiere = form.cleaned_data.get('filiere')
        statut_inscription = form.cleaned_data.get('statut_inscription')
        statut_validation = form.cleaned_data.get('statut_validation')
        recherche = form.cleaned_data.get('recherche')
        
        if filiere:
            etudiants = etudiants.filter(filiere=filiere)
        if statut_inscription:
            etudiants = etudiants.filter(statut_inscription=statut_inscription)
        if statut_validation:
            etudiants = etudiants.filter(statut_validation=statut_validation)
        if recherche:
            etudiants = etudiants.filter(
                Q(nom__icontains=recherche) |
                Q(prenoms__icontains=recherche) |
                Q(numero_matricule__icontains=recherche) |
                Q(cni__icontains=recherche)
            )
    
    paginator = Paginator(etudiants, 20)
    page = request.GET.get('page')
    etudiants = paginator.get_page(page)
    
    # Statistiques
    stats = {
        'total': EtudiantAcademique.objects.count(),
        'en_attente': EtudiantAcademique.objects.filter(statut_validation='en_attente').count(),
        'valides': EtudiantAcademique.objects.filter(statut_validation='valide').count(),
        'rejetes': EtudiantAcademique.objects.filter(statut_validation='rejete').count(),
    }
    
    context = {
        'etudiants': etudiants,
        'form': form,
        'stats': stats,
    }
    
    return render(request, 'academique/admin/etudiants_list.html', context)


@admin_required
def admin_import_etudiants(request):
    """Import d'étudiants via Excel"""
    if request.method == 'POST':
        form = ImportEtudiantForm(request.POST, request.FILES)
        if form.is_valid():
            import_obj = form.save(commit=False)
            import_obj.importe_par = request.user
            import_obj.save()
            
            # Traitement du fichier Excel
            try:
                result = _process_excel_import(import_obj)
                if result['success']:
                    messages.success(request, f'Import réussi: {result["success"]} étudiants importés.')
                if result['errors']:
                    messages.warning(request, f'{result["errors"]} erreurs lors de l\'import.')
                    
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'import: {str(e)}')
                
            return redirect('academique:admin_etudiants_list')
    else:
        form = ImportEtudiantForm()
    
    # Historique des imports
    imports = ImportEtudiant.objects.filter(importe_par=request.user)[:5]
    
    return render(request, 'academique/admin/import_etudiants.html', {
        'form': form,
        'imports': imports
    })


@admin_required
def admin_documents_validation(request):
    """Interface de validation des documents"""
    documents = DocumentEtudiant.objects.select_related(
        'etudiant', 'etudiant__filiere'
    ).filter(valide=False).order_by('-date_upload')
    
    # Filtrage par type
    type_doc = request.GET.get('type')
    if type_doc:
        documents = documents.filter(type_document=type_doc)
    
    paginator = Paginator(documents, 15)
    page = request.GET.get('page')
    documents = paginator.get_page(page)
    
    context = {
        'documents': documents,
        'types_documents': DocumentEtudiant.TYPE_DOCUMENT_CHOICES,
        'selected_type': type_doc,
        'pending_count': DocumentEtudiant.objects.filter(valide=False).count(),
    }
    
    return render(request, 'academique/admin/documents_validation.html', context)


@admin_required
def admin_validate_document(request, doc_id):
    """Validation/rejet d'un document"""
    document = get_object_or_404(DocumentEtudiant, id=doc_id)
    
    if request.method == 'POST':
        form = ValidationDocumentForm(request.POST, instance=document)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.valide_par = request.user if doc.valide else None
            doc.save()
            
            action = "validé" if doc.valide else "rejeté"
            messages.success(request, f'Document {action} avec succès.')
            
            return redirect('academique:admin_documents_validation')
    else:
        form = ValidationDocumentForm(instance=document)
    
    return render(request, 'academique/admin/document_validation_form.html', {
        'form': form,
        'document': document
    })


@admin_required  
def export_etudiants_excel(request):
    """Export des étudiants en Excel"""
    # Créer le workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Étudiants"
    
    # Headers
    headers = [
        'Matricule', 'Nom', 'Prénoms', 'CNI', 'Téléphone', 'Email',
        'Filière', 'Statut Inscription', 'Statut Validation', 'Date Inscription'
    ]
    ws.append(headers)
    
    # Données
    etudiants = EtudiantAcademique.objects.select_related('filiere').all()
    for etudiant in etudiants:
        ws.append([
            etudiant.numero_matricule,
            etudiant.nom,
            etudiant.prenoms,
            etudiant.cni,
            etudiant.telephone,
            etudiant.email_personnel,
            etudiant.filiere.nom,
            etudiant.get_statut_inscription_display(),
            etudiant.get_statut_validation_display(),
            etudiant.date_inscription.strftime('%d/%m/%Y')
        ])
    
    # Réponse HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="etudiants_{timezone.now().strftime("%Y%m%d")}.xlsx"'
    
    wb.save(response)
    return response


# =================== VIEWS ÉTUDIANT ===================

@role_required('ETUDIANT')
def etudiant_inscription(request):
    """Formulaire d'inscription étudiant"""
    try:
        etudiant = request.user.etudiant_academique
        # Si déjà inscrit, rediriger vers le profil
        return redirect('academique:etudiant_profile')
    except EtudiantAcademique.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = EtudiantInscriptionForm(request.POST)
        if form.is_valid():
            etudiant = form.save(commit=False)
            etudiant.user = request.user
            etudiant.nom = request.user.last_name
            etudiant.prenoms = request.user.first_name
            etudiant.save()
            
            messages.success(request, 'Inscription académique enregistrée avec succès!')
            return redirect('academique:etudiant_profile')
    else:
        # Pré-remplir avec les données utilisateur
        initial_data = {
            'nom': request.user.last_name,
            'prenoms': request.user.first_name,
        }
        form = EtudiantInscriptionForm(initial=initial_data)
    
    return render(request, 'academique/etudiant/inscription.html', {'form': form})


@role_required('ETUDIANT')
def etudiant_profile(request):
    """Profil étudiant"""
    try:
        etudiant = request.user.etudiant_academique
    except EtudiantAcademique.DoesNotExist:
        return redirect('academique:etudiant_inscription')
    
    documents = etudiant.documents.all()
    documents_requis = [choice[0] for choice in DocumentEtudiant.TYPE_DOCUMENT_CHOICES]
    documents_manquants = [
        type_doc for type_doc in documents_requis 
        if not documents.filter(type_document=type_doc).exists()
    ]
    
    context = {
        'etudiant': etudiant,
        'documents': documents,
        'documents_manquants': documents_manquants,
        'progression': _calculate_completion_progress(etudiant),
    }
    
    return render(request, 'academique/etudiant/profile.html', context)


@role_required('ETUDIANT')
def etudiant_documents(request):
    """Gestion des documents étudiant"""
    try:
        etudiant = request.user.etudiant_academique
    except EtudiantAcademique.DoesNotExist:
        return redirect('academique:etudiant_inscription')
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Vérifier si le document existe déjà
            existing = DocumentEtudiant.objects.filter(
                etudiant=etudiant,
                type_document=form.cleaned_data['type_document']
            ).first()
            
            if existing:
                # Remplacer le document existant
                existing.fichier = form.cleaned_data['fichier']
                existing.valide = False
                existing.valide_par = None
                existing.commentaire = ''
                existing.save()
                messages.success(request, 'Document remplacé avec succès.')
            else:
                # Nouveau document
                document = form.save(commit=False)
                document.etudiant = etudiant
                document.save()
                messages.success(request, 'Document ajouté avec succès.')
            
            return redirect('academique:etudiant_documents')
    else:
        form = DocumentUploadForm()
    
    documents = etudiant.documents.all()
    
    return render(request, 'academique/etudiant/documents.html', {
        'form': form,
        'documents': documents,
        'etudiant': etudiant
    })


@role_required('ETUDIANT')
def ajax_delete_document(request, doc_id):
    """Suppression AJAX d'un document"""
    if request.method == 'POST':
        try:
            document = DocumentEtudiant.objects.get(
                id=doc_id, 
                etudiant=request.user.etudiant_academique
            )
            document.delete()
            return JsonResponse({'success': True})
        except DocumentEtudiant.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Document non trouvé'})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


@role_required('ETUDIANT')
def etudiant_fiche_pdf(request):
    """Génération de la fiche d'inscription PDF"""
    try:
        etudiant = request.user.etudiant_academique
    except EtudiantAcademique.DoesNotExist:
        messages.error(request, 'Vous devez d\'abord compléter votre inscription.')
        return redirect('academique:etudiant_inscription')
    
    # Créer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fiche_inscription_{etudiant.numero_matricule}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # En-tête
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "FICHE D'INSCRIPTION ACADÉMIQUE")
    
    # Informations étudiant
    y_position = height - 100
    p.setFont("Helvetica", 12)
    
    infos = [
        f"Matricule: {etudiant.numero_matricule}",
        f"Nom complet: {etudiant.nom_complet}",
        f"CNI: {etudiant.cni}",
        f"Téléphone: {etudiant.telephone}",
        f"Email: {etudiant.email_personnel}",
        f"Filière: {etudiant.filiere.nom}",
        f"Date d'inscription: {etudiant.date_inscription.strftime('%d/%m/%Y')}",
    ]
    
    for info in infos:
        p.drawString(50, y_position, info)
        y_position -= 25
    
    p.showPage()
    p.save()
    
    return response


# =================== VIEWS PUBLIQUES ===================

def filieres_list_public(request):
    """Liste publique des filières"""
    filieres = Filiere.objects.filter(statut='active').order_by('nom')
    
    context = {
        'filieres': filieres,
        'total_places': sum(f.places_disponibles for f in filieres),
    }
    
    return render(request, 'academique/public/filieres_list.html', context)


def filiere_detail_public(request, code):
    """Détail public d'une filière"""
    filiere = get_object_or_404(Filiere, code=code, statut='active')
    
    context = {
        'filiere': filiere,
    }
    
    return render(request, 'academique/public/filiere_detail.html', context)


# =================== VIEWS AJAX ===================

@admin_required
def ajax_stats_dashboard(request):
    """Statistiques pour le dashboard"""
    stats = {
        'total_etudiants': EtudiantAcademique.objects.count(),
        'etudiants_valides': EtudiantAcademique.objects.filter(statut_validation='valide').count(),
        'documents_en_attente': DocumentEtudiant.objects.filter(valide=False).count(),
        'filieres_actives': Filiere.objects.filter(statut='active').count(),
    }
    
    return JsonResponse(stats)


# =================== FONCTIONS UTILITAIRES ===================

def _process_excel_import(import_obj):
    """Traite l'import Excel des étudiants"""
    try:
        df = pd.read_excel(import_obj.fichier.path)
        
        success_count = 0
        error_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Créer l'utilisateur
                username = f"etudiant_{row['cni']}"
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': row['prenoms'],
                        'last_name': row['nom'],
                        'email': row['email'],
                        'role': 'ETUDIANT'
                    }
                )
                
                if created:
                    user.set_password('password123')  # Mot de passe temporaire
                    user.save()
                
                # Créer l'étudiant académique
                filiere = Filiere.objects.get(code=row['filiere_code'])
                
                etudiant, created = EtudiantAcademique.objects.get_or_create(
                    user=user,
                    defaults={
                        'filiere': filiere,
                        'nom': row['nom'],
                        'prenoms': row['prenoms'],
                        'cni': row['cni'],
                        'telephone': row['telephone'],
                        'email_personnel': row['email'],
                        'date_naissance': row['date_naissance'],
                        'lieu_naissance': row['lieu_naissance'],
                    }
                )
                
                if created:
                    success_count += 1
                
            except Exception as e:
                error_count += 1
                errors.append(f"Ligne {index + 2}: {str(e)}")
        
        # Mettre à jour l'objet import
        import_obj.nombre_total = len(df)
        import_obj.nombre_succes = success_count
        import_obj.nombre_erreurs = error_count
        import_obj.rapport_erreurs = '\n'.join(errors)
        import_obj.save()
        
        return {
            'success': success_count,
            'errors': error_count,
            'details': errors
        }
        
    except Exception as e:
        import_obj.rapport_erreurs = str(e)
        import_obj.save()
        raise e


def _calculate_completion_progress(etudiant):
    """Calcule le pourcentage de completion du profil"""
    total_fields = 10  # Nombre de champs importants
    completed_fields = 0
    
    # Vérifier les champs obligatoires
    if etudiant.date_naissance:
        completed_fields += 1
    if etudiant.lieu_naissance:
        completed_fields += 1
    if etudiant.cni:
        completed_fields += 1
    if etudiant.telephone:
        completed_fields += 1
    if etudiant.email_personnel:
        completed_fields += 1
    if etudiant.adresse:
        completed_fields += 1
    if etudiant.nom_pere:
        completed_fields += 1
    if etudiant.nom_mere:
        completed_fields += 1
    if etudiant.diplome_obtenu:
        completed_fields += 1
    if etudiant.annee_obtention:
        completed_fields += 1
    
    return int((completed_fields / total_fields) * 100)