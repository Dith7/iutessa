from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
import json
import os
from pages.models import PageBlock
from .forms import PageBlockForm, MediaUploadForm
from datetime import timedelta
from django.utils import timezone

# Importer les décorateurs du module users
from users.decorators import admin_required, role_required



@admin_required
def dashboard_view(request):
    """Dashboard principal avec statistiques et module académique"""
    from django.contrib.auth import get_user_model
    from django.conf import settings
    from django.utils import timezone
    from datetime import timedelta
    from academique.models import Filiere, EtudiantAcademique, DocumentEtudiant
    
    User = get_user_model()
    
    # Statistiques des blocs (existantes)
    stats = {
        'total_blocks': PageBlock.objects.count(),
        'active_blocks': PageBlock.objects.filter(status='active').count(),
        'inactive_blocks': PageBlock.objects.filter(status='inactive').count(),
        'blocks_with_media': PageBlock.objects.filter(
            Q(image__isnull=False) | 
            Q(document__isnull=False) | 
            Q(video_file__isnull=False) | 
            Q(video_url__isnull=False)
        ).count(),
    }
    
    # Statistiques des utilisateurs (existantes)
    user_stats = {
        'total_users': User.objects.count(),
        'admin_count': User.objects.filter(role='ADMIN').count(),
        'etudiant_count': User.objects.filter(role='ETUDIANT').count(),
        'visiteur_count': User.objects.filter(role='VISITEUR').count(),
        'active_users': User.objects.filter(is_active=True).count(),
    }
    
    # NOUVELLES STATISTIQUES ACADÉMIQUES
    academic_stats = {
        'total_filieres': Filiere.objects.count(),
        'filieres_actives': Filiere.objects.filter(statut='active').count(),
        'total_etudiants': EtudiantAcademique.objects.count(),
        'etudiants_en_attente': EtudiantAcademique.objects.filter(statut_validation='en_attente').count(),
        'etudiants_valides': EtudiantAcademique.objects.filter(statut_validation='valide').count(),
        'documents_en_attente': DocumentEtudiant.objects.filter(valide=False).count(),
        'taux_validation': 0
    }
    
    # Calcul du taux de validation
    if academic_stats['total_etudiants'] > 0:
        academic_stats['taux_validation'] = (
            academic_stats['etudiants_valides'] / academic_stats['total_etudiants']
        ) * 100
    
    # Top 5 filières par nombre d'étudiants
    top_filieres = Filiere.objects.annotate(
        nb_etudiants=Count('etudiants')
    ).order_by('-nb_etudiants')[:5]
    
    # Évolution des inscriptions (7 derniers jours)
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
    
    # Blocs par type (existants)
    blocks_by_type = (
        PageBlock.objects
        .values('block_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    # Derniers blocs modifiés (existants)
    recent_blocks = (
        PageBlock.objects
        .order_by('-updated_at')[:5]
    )
    
    # Derniers utilisateurs créés (existants)
    recent_users = (
        User.objects
        .order_by('-date_joined')[:5]
    )
    
    # NOUVEAUX : Derniers étudiants inscrits
    recent_etudiants = (
        EtudiantAcademique.objects
        .select_related('filiere')
        .order_by('-date_inscription')[:5]
    )
    
    # Taille média (existante)
    media_size = _calculate_media_size()
    
    # Mode debug (existant)
    debug = getattr(settings, 'DEBUG', False)
    
    context = {
        # Données existantes
        'stats': stats,
        'user_stats': user_stats,
        'blocks_by_type': blocks_by_type,
        'recent_blocks': recent_blocks,
        'recent_users': recent_users,
        'media_size': media_size,
        'debug': debug,
        
        # NOUVELLES DONNÉES ACADÉMIQUES
        'academic_stats': academic_stats,
        'top_filieres': top_filieres,
        'inscriptions_semaine': inscriptions_semaine,
        'recent_etudiants': recent_etudiants,
    }
    
    return render(request, 'administration/dashboard.html', context)


def _calculate_media_size():
    """Calcule la taille des médias en MB"""
    import os
    from django.conf import settings
    
    try:
        media_root = settings.MEDIA_ROOT
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(media_root):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return round(total_size / (1024 * 1024), 2)
    except:
        return 0

@admin_required
def blocks_list_view(request):
    """Liste des blocs avec recherche et filtres"""
    blocks = PageBlock.objects.all()
    
    # Recherche
    search = request.GET.get('search')
    if search:
        blocks = blocks.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(subtitle__icontains=search)
        )
    
    # Filtres
    block_type = request.GET.get('type')
    if block_type:
        blocks = blocks.filter(block_type=block_type)
    
    status = request.GET.get('status')
    if status:
        blocks = blocks.filter(status=status)
    
    # Tri
    sort_by = request.GET.get('sort', '-updated_at')
    blocks = blocks.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(blocks, 12)
    page = request.GET.get('page')
    blocks = paginator.get_page(page)
    
    context = {
        'blocks': blocks,
        'block_types': PageBlock.BLOCK_TYPE_CHOICES,
        'current_filters': {
            'search': search,
            'type': block_type,
            'status': status,
            'sort': sort_by,
        }
    }
    
    return render(request, 'administration/blocks/list.html', context)


@admin_required
def block_create_view(request):
    """Créer un nouveau bloc"""
    if request.method == 'POST':
        form = PageBlockForm(request.POST, request.FILES)
        if form.is_valid():
            block = form.save()
            messages.success(request, f'Bloc "{block.title}" créé avec succès.')
            return redirect('administration:block_detail', pk=block.pk)
    else:
        form = PageBlockForm()
    
    context = {
        'form': form,
        'title': 'Créer un nouveau bloc',
        'action_url': reverse_lazy('administration:block_create'),
    }
    
    return render(request, 'administration/blocks/form.html', context)


@admin_required
def block_detail_view(request, pk):
    """Détail et édition d'un bloc"""
    block = get_object_or_404(PageBlock, pk=pk)
    
    context = {
        'block': block,
        'preview_url': f"/?preview_block={block.pk}",
    }
    
    return render(request, 'administration/blocks/detail.html', context)


@admin_required
def block_update_view(request, pk):
    """Modifier un bloc"""
    block = get_object_or_404(PageBlock, pk=pk)
    
    if request.method == 'POST':
        form = PageBlockForm(request.POST, request.FILES, instance=block)
        if form.is_valid():
            block = form.save()
            messages.success(request, f'Bloc "{block.title}" modifié avec succès.')
            return redirect('administration:block_detail', pk=block.pk)
    else:
        form = PageBlockForm(instance=block)
    
    context = {
        'form': form,
        'block': block,
        'title': f'Modifier "{block.title}"',
        'action_url': reverse_lazy('administration:block_update', kwargs={'pk': pk}),
    }
    
    return render(request, 'administration/blocks/form.html', context)


@admin_required
def block_delete_view(request, pk):
    """Supprimer un bloc"""
    block = get_object_or_404(PageBlock, pk=pk)
    
    if request.method == 'POST':
        block_title = block.title
        block.delete()
        messages.success(request, f'Bloc "{block_title}" supprimé avec succès.')
        return redirect('administration:blocks_list')
    
    context = {
        'block': block,
        'title': f'Supprimer "{block.title}"',
    }
    
    return render(request, 'administration/blocks/delete.html', context)


@admin_required
@require_http_methods(["POST"])
def block_toggle_status_view(request, pk):
    """Activer/désactiver un bloc (AJAX)"""
    block = get_object_or_404(PageBlock, pk=pk)
    
    new_status = 'active' if block.status == 'inactive' else 'inactive'
    block.status = new_status
    block.save()
    
    return JsonResponse({
        'success': True,
        'status': new_status,
        'message': f'Bloc {new_status}',
    })


@admin_required
@require_http_methods(["POST"])
def blocks_reorder_view(request):
    """Réorganiser l'ordre des blocs (AJAX)"""
    try:
        data = json.loads(request.body)
        block_orders = data.get('orders', [])
        
        for item in block_orders:
            block_id = item.get('id')
            new_order = item.get('order')
            
            PageBlock.objects.filter(pk=block_id).update(order=new_order)
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@admin_required
def media_library_view(request):
    """Bibliothèque des médias"""
    # Images - filtrer pour éviter les erreurs de fichiers manquants
    images = PageBlock.objects.filter(
        image__isnull=False
    ).exclude(image__exact='').order_by('-updated_at')
    
    # Documents
    documents = PageBlock.objects.filter(
        document__isnull=False
    ).exclude(document__exact='').order_by('-updated_at')
    
    # Vidéos
    videos = PageBlock.objects.filter(
        Q(video_file__isnull=False) | Q(video_url__isnull=False)
    ).order_by('-updated_at')
    
    # Statistiques médias
    media_stats = {
        'images_count': images.count(),
        'documents_count': documents.count(),
        'videos_count': videos.count(),
        'total_size': _calculate_media_size(),
    }
    
    context = {
        'images': images[:20],  # Pagination à implémenter
        'documents': documents[:20],
        'videos': videos[:20],
        'media_stats': media_stats,
    }
    
    return render(request, 'administration/media/library.html', context)


@admin_required
@require_http_methods(["POST"])
def media_upload_view(request):
    """Upload de médias (AJAX)"""
    form = MediaUploadForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Traitement selon le type de fichier
        uploaded_file = request.FILES['file']
        
        # Sauvegarder et retourner infos
        file_path = default_storage.save(uploaded_file.name, uploaded_file)
        file_url = default_storage.url(file_path)
        
        return JsonResponse({
            'success': True,
            'file_url': file_url,
            'file_name': uploaded_file.name,
            'file_size': uploaded_file.size,
        })
    
    return JsonResponse({
        'success': False,
        'errors': form.errors,
    })


@admin_required
def settings_view(request):
    """Paramètres du site"""
    from pages.models import SiteSettings
    
    if request.method == 'POST':
        # Traitement des paramètres
        site_settings = SiteSettings.get_settings()
        
        # Mise à jour des champs depuis le formulaire
        site_settings.site_name = request.POST.get('site_name', site_settings.site_name)
        site_settings.site_description = request.POST.get('site_description', site_settings.site_description)
        site_settings.contact_email = request.POST.get('contact_email', site_settings.contact_email)
        site_settings.contact_phone = request.POST.get('phone', site_settings.contact_phone)
        site_settings.meta_description = request.POST.get('meta_description', site_settings.meta_description)
        site_settings.meta_keywords = request.POST.get('meta_keywords', site_settings.meta_keywords)
        site_settings.google_analytics_id = request.POST.get('google_analytics', site_settings.google_analytics_id)
        
        # Options booléennes
        site_settings.show_contact_info = 'show_contact_info' in request.POST
        site_settings.maintenance_mode = 'maintenance_mode' in request.POST
        
        site_settings.save()
        
        messages.success(request, 'Paramètres sauvegardés avec succès.')
        return redirect('administration:settings')
    
    context = {
        'site_info': _get_site_info(),
        'site_settings': SiteSettings.get_settings(),
    }
    
    return render(request, 'administration/settings.html', context)


@admin_required
def preview_site_view(request):
    """Preview du site public dans iframe"""
    return render(request, 'administration/preview.html')


@admin_required
def analytics_view(request):
    """Analytics et statistiques avancées"""
    # Stats par période
    stats_data = _get_analytics_data()
    
    context = {
        'stats_data': stats_data,
    }
    
    return render(request, 'administration/analytics.html', context)


# Vue accessible aux étudiants et admins pour consulter leurs propres données
@role_required('ADMIN', 'ETUDIANT')
def user_analytics_view(request):
    """Analytics pour les étudiants (leurs propres données)"""
    if request.user.is_admin():
        # Les admins voient tout
        return redirect('administration:analytics')
    
    # Pour les étudiants : stats personnelles
    context = {
        'user_stats': _get_user_personal_stats(request.user),
    }
    
    return render(request, 'administration/user_analytics.html', context)


# Méthodes utilitaires privées

def _calculate_media_size():
    """Calculer la taille totale des médias"""
    total_size = 0
    
    # Parcourir tous les blocs avec médias
    blocks_with_media = PageBlock.objects.filter(
        Q(image__isnull=False) | 
        Q(document__isnull=False) | 
        Q(video_file__isnull=False)
    )
    
    for block in blocks_with_media:
        try:
            if block.image and default_storage.exists(block.image.name):
                total_size += block.image.size
        except:
            pass
        
        try:
            if block.document and default_storage.exists(block.document.name):
                total_size += block.document.size
        except:
            pass
        
        try:
            if block.video_file and default_storage.exists(block.video_file.name):
                total_size += block.video_file.size
        except:
            pass
    
    # Convertir en MB
    return round(total_size / (1024 * 1024), 2)


def _get_site_info():
    """Informations générales du site"""
    return {
        'total_blocks': PageBlock.objects.count(),
        'active_blocks': PageBlock.objects.filter(status='active').count(),
        'media_size': _calculate_media_size(),
        'last_update': PageBlock.objects.order_by('-updated_at').first(),
    }


def _get_analytics_data():
    """Données analytiques avancées"""
    return {
        'blocks_created_last_30_days': PageBlock.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
        'most_used_block_types': (
            PageBlock.objects
            .values('block_type')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        ),
        'blocks_by_status': {
            'active': PageBlock.objects.filter(status='active').count(),
            'inactive': PageBlock.objects.filter(status='inactive').count(),
        }
    }


def _get_user_personal_stats(user):
    """Stats personnelles pour un étudiant"""
    # À implémenter selon les besoins du module académique
    return {
        'courses_enrolled': 0,
        'assignments_completed': 0,
        'average_grade': 0,
    }