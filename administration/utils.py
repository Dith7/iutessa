# administration/utils.py (nouveau fichier)

import re

def format_simple_text(text):
    """
    Convertit le texte simple en HTML formaté
    """
    if not text:
        return ""
    
    lines = text.split('\n')
    formatted_lines = []
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Ligne vide = nouveau paragraphe
        if not line:
            if current_section:
                formatted_lines.append('</div>')
                current_section = None
            formatted_lines.append('')
            continue
        
        # Détection titre avec emoji (emoji au début + texte)
        emoji_title_match = re.match(r'^([🎬🎓👨‍🏫🔬📚💼🏆🌟📊🎯]+)\s+(.+)$', line)
        if emoji_title_match:
            if current_section:
                formatted_lines.append('</div>')
            emoji, title = emoji_title_match.groups()
            formatted_lines.append(f'<div class="mb-6">')
            formatted_lines.append(f'    <h4 class="text-lg font-semibold text-gray-900 mb-2">{emoji} {title}</h4>')
            current_section = True
            continue
        
        # Détection liste avec tirets
        if line.startswith('- ') or line.startswith('• '):
            content = line[2:].strip()
            if not current_section:
                formatted_lines.append('<ul class="list-disc list-inside mb-4 space-y-1">')
                current_section = 'list'
            formatted_lines.append(f'    <li class="text-gray-700">{content}</li>')
            continue
        
        # Fermer liste si on sort d'une liste
        if current_section == 'list':
            formatted_lines.append('</ul>')
            current_section = None
        
        # Paragraphe normal
        if current_section == True:  # Dans une section avec titre
            formatted_lines.append(f'    <p class="text-gray-700">{line}</p>')
        else:
            formatted_lines.append(f'<p class="text-gray-700 mb-4">{line}</p>')
    
    # Fermer la dernière section
    if current_section == True:
        formatted_lines.append('</div>')
    elif current_section == 'list':
        formatted_lines.append('</ul>')
    
    return '\n'.join(formatted_lines)