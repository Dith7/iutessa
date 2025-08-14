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
