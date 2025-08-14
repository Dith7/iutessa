from django.conf import settings
from pages.models import PageBlock

def admin_context(request):
    """Context processor pour variables globales de l'administration"""
    
    if not request.path.startswith('/administration/'):
        return {}
    
    return {
        'admin_config': getattr(settings, 'ADMINISTRATION_CONFIG', {}),
        'total_blocks': PageBlock.objects.count(),
        'active_blocks': PageBlock.objects.filter(status='active').count(),
        'debug': settings.DEBUG,
    }