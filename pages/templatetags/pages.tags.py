# pages/templatetags/pages_tags.py
from django import template
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

register = template.Library()

@register.inclusion_tag('pages/blocks/default.html', takes_context=True)
def render_block(context, block):
    """
    Render un bloc avec le bon template ou fallback vers default.html
    """
    # Essayer le template spécifique au type de bloc
    template_name = f'pages/blocks/{block.block_type}.html'
    
    try:
        # Vérifier si le template existe
        get_template(template_name)
        context['template_name'] = template_name
    except TemplateDoesNotExist:
        # Fallback vers le template par défaut
        context['template_name'] = 'pages/blocks/default.html'
        print(f"⚠️ Template {template_name} non trouvé, utilisation du template par défaut")
    
    context['block'] = block
    return context

from django import template
from academique.models import Filiere

register = template.Library()

@register.simple_tag
def get_public_filieres():
    """Récupère les filières actives pour affichage public"""
    return Filiere.objects.filter(statut='active').order_by('nom')

@register.simple_tag
def get_filieres_count():
    """Retourne le nombre total de filières actives"""
    return Filiere.objects.filter(statut='active').count()

@register.simple_tag
def get_total_places():
    """Retourne le nombre total de places disponibles"""
    filieres = Filiere.objects.filter(statut='active')
    return sum(f.places_disponibles for f in filieres)
