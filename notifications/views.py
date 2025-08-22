# notifications/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Notification, PreferenceNotification
from .services import NotificationService

@login_required
def notification_list(request):
    """Liste des notifications avec filtres"""
    notifications = request.user.notifications.all()
    
    # Filtrage
    filter_type = request.GET.get('type', '')
    filter_priority = request.GET.get('priority', '')
    filter_read = request.GET.get('read', '')
    
    if filter_type:
        notifications = notifications.filter(type_notification=filter_type)
    if filter_priority:
        notifications = notifications.filter(priorite=filter_priority)
    if filter_read:
        if filter_read == 'unread':
            notifications = notifications.filter(lu=False)
        elif filter_read == 'read':
            notifications = notifications.filter(lu=True)
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)
    
    # Stats
    stats = {
        'total': request.user.notifications.count(),
        'non_lues': request.user.notifications.filter(lu=False).count(),
        'urgentes': request.user.notifications.filter(priorite__in=['haute', 'urgente'], lu=False).count(),
    }
    
    context = {
        'notifications': notifications,
        'stats': stats,
        'filter_type': filter_type,
        'filter_priority': filter_priority,
        'filter_read': filter_read,
    }
    
    return render(request, 'notifications/notification_list.html', context)


@login_required
def notification_detail(request, pk):
    """Détail d'une notification"""
    notification = get_object_or_404(Notification, pk=pk, destinataire=request.user)
    
    # Marquer comme lue
    notification.marquer_comme_lu()
    
    return render(request, 'notifications/notification_detail.html', {
        'notification': notification
    })


@login_required
def notification_preferences(request):
    """Gestion des préférences de notification"""
    preferences, created = PreferenceNotification.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Mise à jour des préférences
        preferences.email_inscription = request.POST.get('email_inscription') == 'on'
        preferences.email_documents = request.POST.get('email_documents') == 'on'
        preferences.email_validation = request.POST.get('email_validation') == 'on'
        preferences.email_rappels = request.POST.get('email_rappels') == 'on'
        preferences.email_info = request.POST.get('email_info') == 'on'
        preferences.push_enabled = request.POST.get('push_enabled') == 'on'
        preferences.frequence_email = request.POST.get('frequence_email', 'immediate')
        preferences.save()
        
        return JsonResponse({'success': True, 'message': 'Préférences mises à jour'})
    
    return render(request, 'notifications/preferences.html', {
        'preferences': preferences
    })


@login_required
def ajax_mark_as_read(request):
    """Marque une ou plusieurs notifications comme lues"""
    if request.method == 'POST':
        notification_ids = request.POST.getlist('ids[]')
        if notification_ids:
            Notification.objects.filter(
                id__in=notification_ids, 
                destinataire=request.user
            ).update(lu=True, date_lecture=timezone.now())
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def ajax_mark_all_read(request):
    """Marque toutes les notifications comme lues"""
    if request.method == 'POST':
        request.user.notifications.filter(lu=False).update(
            lu=True, 
            date_lecture=timezone.now()
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def ajax_delete_notification(request, pk):
    """Supprime une notification"""
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(pk=pk, destinataire=request.user)
            notification.delete()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification non trouvée'})
    return JsonResponse({'success': False})


@login_required
def ajax_unread_count(request):
    """Retourne le nombre de notifications non lues"""
    count = request.user.notifications.filter(lu=False).count()
    urgent_count = request.user.notifications.filter(
        lu=False, 
        priorite__in=['haute', 'urgente']
    ).count()
    
    return JsonResponse({
        'unread_count': count,
        'urgent_count': urgent_count
    })


@login_required
def ajax_recent_notifications(request):
    """Retourne les notifications récentes pour l'affichage en dropdown"""
    notifications = request.user.notifications.filter(lu=False)[:5]
    
    data = [{
        'id': n.id,
        'titre': n.titre,
        'message': n.message[:100],
        'type': n.type_notification,
        'priorite': n.priorite,
        'icone': n.icone,
        'date': n.date_creation.strftime('%d/%m %H:%M'),
        'url': n.url_action
    } for n in notifications]
    
    return JsonResponse({'notifications': data})