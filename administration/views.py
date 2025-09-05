# administration/views.py
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import reverse_lazy
import json
from datetime import timedelta
from django.utils import timezone
from notifications.services import NotificationService
from users.decorators import admin_required, role_required


@admin_required
def dashboard_view(request):
    """Dashboard administration centré sur l'académique"""
    from django.contrib.auth import get_user_model
    from academique.models import Filiere, EtudiantAcademique, DocumentEtudiant
    
    User = get_user_model()
    
    # Statistiques utilisateurs
    user_stats = {
        'total_users': User.objects.count(),
        'admin_count': User.objects.filter(role='ADMIN').count(),
        'etudiant_count': User.objects.filter(role='ETUDIANT').count(),
        'visiteur_count': User.objects.filter(role='VISITEUR').count(),
        'active_users': User.objects.filter(is_active=True).count(),
    }
    
    # Statistiques académiques principales
    academic_stats = {
        'total_filieres': Filiere.objects.count(),
        'filieres_actives': Filiere.objects.filter(statut='active').count(),
        'total_etudiants': EtudiantAcademique.objects.count(),
        'etudiants_en_attente': EtudiantAcademique.objects.filter(statut_validation='en_attente').count(),
        'etudiants_valides': EtudiantAcademique.objects.filter(statut_validation='valide').count(),
        'etudiants_rejetes': EtudiantAcademique.objects.filter(statut_validation='rejete').count(),
        'documents_en_attente': DocumentEtudiant.objects.filter(valide=False).count(),
        'documents_valides': DocumentEtudiant.objects.filter(valide=True).count(),
        'taux_validation': 0
    }
    
    # Calcul du taux de validation
    if academic_stats['total_etudiants'] > 0:
        academic_stats['taux_validation'] = (
            academic_stats['etudiants_valides'] / academic_stats['total_etudiants']
        ) * 100
    
    # Notification pour documents en attente
    if academic_stats['documents_en_attente'] > 10 and not request.session.get('docs_reminder_sent'):
        NotificationService.create_notification(
            destinataire=request.user,
            type_notification='rappel',
            titre='Documents en attente de validation',
            message=f'{academic_stats["documents_en_attente"]} documents nécessitent votre attention',
            priorite='haute',
            url_action='/academique/administration/documents/'
        )
        request.session['docs_reminder_sent'] = True
    
    # Top filières par étudiants
    top_filieres = Filiere.objects.annotate(
        nb_etudiants=Count('etudiants')
    ).order_by('-nb_etudiants')[:5]
    
    # Évolution inscriptions (7 derniers jours)
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    inscriptions_semaine = []
    for i in range(7):
        date = week_ago + timedelta(days=i)
        count = EtudiantAcademique.objects.filter(
            date_inscription__date=date
        ).count()
        inscriptions_semaine.append({
            'date': date.strftime('%d/%m'),
            'count': count
        })
    
    # Derniers étudiants inscrits
    recent_etudiants = EtudiantAcademique.objects.select_related(
        'filiere', 'user'
    ).order_by('-date_inscription')[:10]
    
    # Documents récents
    recent_documents = DocumentEtudiant.objects.select_related(
        'etudiant', 'etudiant__filiere'
    ).order_by('-date_upload')[:10]
    
    # Statistiques par filière
    filieres_stats = []
    for filiere in Filiere.objects.filter(statut='active'):
        filieres_stats.append({
            'filiere': filiere,
            'etudiants': filiere.etudiants.count(),
            'en_attente': filiere.etudiants.filter(statut_validation='en_attente').count(),
            'valides': filiere.etudiants.filter(statut_validation='valide').count(),
            'taux_occupation': filiere.taux_occupation,
        })
    
    context = {
        'user_stats': user_stats,
        'academic_stats': academic_stats,
        'top_filieres': top_filieres,
        'inscriptions_semaine': inscriptions_semaine,
        'recent_etudiants': recent_etudiants,
        'recent_documents': recent_documents,
        'filieres_stats': filieres_stats,
        'debug': getattr(settings, 'DEBUG', False),
    }
    
    return render(request, 'administration/dashboard.html', context)


@admin_required
def academic_overview(request):
    """Vue d'ensemble académique détaillée"""
    from academique.models import Filiere, EtudiantAcademique, DocumentEtudiant
    
    # Filtres
    filiere_filter = request.GET.get('filiere')
    statut_filter = request.GET.get('statut')
    
    etudiants = EtudiantAcademique.objects.select_related('filiere', 'user')
    
    if filiere_filter:
        etudiants = etudiants.filter(filiere_id=filiere_filter)
    if statut_filter:
        etudiants = etudiants.filter(statut_validation=statut_filter)
    
    # Pagination
    paginator = Paginator(etudiants.order_by('-date_inscription'), 20)
    page = request.GET.get('page')
    etudiants = paginator.get_page(page)
    
    context = {
        'etudiants': etudiants,
        'filieres': Filiere.objects.filter(statut='active'),
        'current_filters': {
            'filiere': filiere_filter,
            'statut': statut_filter,
        },
        'statut_choices': EtudiantAcademique.STATUT_VALIDATION_CHOICES,
    }
    
    return render(request, 'administration/academic_overview.html', context)


@admin_required
def documents_validation(request):
    """Validation des documents étudiants"""
    from academique.models import DocumentEtudiant
    
    # Documents en attente
    documents = DocumentEtudiant.objects.filter(
        valide=False
    ).select_related('etudiant', 'etudiant__filiere').order_by('-date_upload')
    
    # Filtres
    type_filter = request.GET.get('type')
    filiere_filter = request.GET.get('filiere')
    
    if type_filter:
        documents = documents.filter(type_document=type_filter)
    if filiere_filter:
        documents = documents.filter(etudiant__filiere_id=filiere_filter)
    
    # Pagination
    paginator = Paginator(documents, 20)
    page = request.GET.get('page')
    documents = paginator.get_page(page)
    
    context = {
        'documents': documents,
        'types_documents': DocumentEtudiant.TYPE_DOCUMENT_CHOICES,
        'current_filters': {
            'type': type_filter,
            'filiere': filiere_filter,
        }
    }
    
    return render(request, 'administration/documents_validation.html', context)


@admin_required
@require_http_methods(["POST"])
def validate_document(request, document_id):
    """Valider/rejeter un document"""
    from academique.models import DocumentEtudiant
    
    document = get_object_or_404(DocumentEtudiant, id=document_id)
    action = request.POST.get('action')
    commentaire = request.POST.get('commentaire', '')
    
    if action == 'validate':
        document.valide = True
        document.valide_par = request.user
        document.commentaire = commentaire
        document.save()
        
        # Notification à l'étudiant
        NotificationService.create_notification(
            destinataire=document.etudiant.user,
            expediteur=request.user,
            type_notification='validation',
            titre='Document validé',
            message=f'Votre {document.get_type_document_display()} a été validé',
            priorite='normale'
        )
        
        messages.success(request, 'Document validé avec succès.')
        
    elif action == 'reject':
        document.valide = False
        document.commentaire = commentaire
        document.save()
        
        # Notification à l'étudiant
        NotificationService.create_notification(
            destinataire=document.etudiant.user,
            expediteur=request.user,
            type_notification='rejet',
            titre='Document rejeté',
            message=f'Votre {document.get_type_document_display()} a été rejeté. Raison: {commentaire}',
            priorite='haute'
        )
        
        messages.warning(request, 'Document rejeté.')
    
    return redirect('administration:documents_validation')


@admin_required
def filieres_management(request):
    """Gestion des filières"""
    from academique.models import Filiere
    
    filieres = Filiere.objects.annotate(
        nb_etudiants=Count('etudiants')
    ).order_by('nom')
    
    # Filtres
    search = request.GET.get('search')
    if search:
        filieres = filieres.filter(
            Q(nom__icontains=search) | Q(code__icontains=search)
        )
    
    context = {
        'filieres': filieres,
        'search': search,
    }
    
    return render(request, 'administration/filieres_management.html', context)


@admin_required
def statistics_view(request):
    """Statistiques avancées"""
    from academique.models import Filiere, EtudiantAcademique, DocumentEtudiant
    from django.db.models import Count, Avg
    
    # Stats par filière
    filieres_data = Filiere.objects.annotate(
        total_etudiants=Count('etudiants'),
        etudiants_valides=Count('etudiants', filter=Q(etudiants__statut_validation='valide')),
        etudiants_attente=Count('etudiants', filter=Q(etudiants__statut_validation='en_attente'))
    ).order_by('-total_etudiants')
    
    # Évolution des inscriptions par mois
    from django.db.models.functions import TruncMonth
    inscriptions_monthly = EtudiantAcademique.objects.annotate(
        mois=TruncMonth('date_inscription')
    ).values('mois').annotate(count=Count('id')).order_by('mois')
    
    # Stats documents
    docs_stats = {
        'total': DocumentEtudiant.objects.count(),
        'valides': DocumentEtudiant.objects.filter(valide=True).count(),
        'en_attente': DocumentEtudiant.objects.filter(valide=False).count(),
    }
    
    # Documents par type
    docs_by_type = DocumentEtudiant.objects.values(
        'type_document'
    ).annotate(count=Count('id')).order_by('-count')
    
    context = {
        'filieres_data': filieres_data,
        'inscriptions_monthly': inscriptions_monthly,
        'docs_stats': docs_stats,
        'docs_by_type': docs_by_type,
    }
    
    return render(request, 'administration/statistics.html', context)


@admin_required
def settings_view(request):
    """Paramètres système"""
    if request.method == 'POST':
        # Traitement des paramètres
        messages.success(request, 'Paramètres sauvegardés.')
        return redirect('administration:settings')
    
    context = {
        'site_name': getattr(settings, 'SITE_NAME', 'IUTESSA'),
        'debug': getattr(settings, 'DEBUG', False),
    }
    
    return render(request, 'administration/settings.html', context)


# Utilitaires
def _get_academic_summary():
    """Résumé académique pour le dashboard"""
    from academique.models import Filiere, EtudiantAcademique, DocumentEtudiant
    
    return {
        'filieres_count': Filiere.objects.filter(statut='active').count(),
        'etudiants_total': EtudiantAcademique.objects.count(),
        'documents_pending': DocumentEtudiant.objects.filter(valide=False).count(),
        'validation_rate': _calculate_validation_rate(),
    }


def _calculate_validation_rate():
    """Calcul du taux de validation global"""
    from academique.models import EtudiantAcademique
    
    total = EtudiantAcademique.objects.count()
    if total == 0:
        return 0
    
    valides = EtudiantAcademique.objects.filter(statut_validation='valide').count()
    return round((valides / total) * 100, 1)