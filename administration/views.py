from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
import json
import os
from pages.models import PageBlock
from .forms import PageBlockForm, MediaUploadForm
from datetime import timedelta
from django.utils import timezone


def is_admin_user(user):
    """Vérifier si l'utilisateur est admin"""
    return user.is_authenticated and user.is_staff


# Décorateur pour toutes les vues admin
admin_required = user_passes_test(is_admin_user, login_url='/admin/login/')


@admin_required
def dashboard_view(request):
    """Dashboard principal avec statistiques"""
    # Statistiques générales
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
    
    # Blocs par type
    blocks_by_type = (
        PageBlock.objects
        .values('block_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    # Derniers blocs modifiés
    recent_blocks = (
        PageBlock.objects
        .order_by('-updated_at')[:5]
    )
    
    # Taille média
    media_size = _calculate_media_size()
    
    context = {
        'stats': stats,
        'blocks_by_type': blocks_by_type,
        'recent_blocks': recent_blocks,
        'media_size': media_size,
    }
    
    return render(request, 'administration/dashboard.html', context)


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
        'block_types': PageBlock.BLOCK_TYPES,
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
    # Images
    images = PageBlock.objects.filter(image__isnull=False).order_by('-updated_at')
    
    # Documents
    documents = PageBlock.objects.filter(document__isnull=False).order_by('-updated_at')
    
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
    if request.method == 'POST':
        # Traitement des paramètres
        messages.success(request, 'Paramètres sauvegardés avec succès.')
        return redirect('administration:settings')
    
    context = {
        'site_info': _get_site_info(),
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
        if block.image and default_storage.exists(block.image.name):
            total_size += block.image.size
        if block.document and default_storage.exists(block.document.name):
            total_size += block.document.size
        if block.video_file and default_storage.exists(block.video_file.name):
            total_size += block.video_file.size
    
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