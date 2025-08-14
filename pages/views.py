from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from .models import PageBlock
import logging

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer tous les blocs actifs triés par ordre
        page_blocks = PageBlock.objects.filter(
            status='active'
        ).order_by('order', 'created_at')
        
        # Vérifier que tous les templates existent
        for block in page_blocks:
            template_name = f'pages/blocks/{block.block_type}.html'
            try:
                get_template(template_name)
            except TemplateDoesNotExist:
                logger.warning(f"Template {template_name} non trouvé pour le bloc {block.id}")
                # On peut soit changer le type vers 'default', soit créer le template
                # Pour l'instant, on log juste l'erreur
        
        context['page_blocks'] = page_blocks
        
        # Grouper les blocs par type pour un affichage plus organisé
        blocks_by_type = {}
        for block in page_blocks:
            if block.block_type not in blocks_by_type:
                blocks_by_type[block.block_type] = []
            blocks_by_type[block.block_type].append(block)
        
        context['blocks_by_type'] = blocks_by_type
        
        return context

def home_view(request):
    """Vue fonction alternative pour la page d'accueil"""
    page_blocks = PageBlock.objects.filter(status='active').order_by('order', 'created_at')
    
    # Vérifier les templates et log les erreurs
    for block in page_blocks:
        template_name = f'pages/blocks/{block.block_type}.html'
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            logger.warning(f"Template {template_name} manquant pour bloc {block.id}")
    
    context = {
        'page_blocks': page_blocks,
        'title': 'Accueil - Université',
    }
    
    return render(request, 'pages/home.html', context)