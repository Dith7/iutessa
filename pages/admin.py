from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import PageBlock

@admin.register(PageBlock)
class PageBlockAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'block_type', 'status', 'order', 
        'preview_media', 'has_document', 'has_video', 'created_at'
    ]
    list_filter = ['block_type', 'status', 'video_type', 'created_at']
    search_fields = ['title', 'subtitle', 'content', 'document_title']
    list_editable = ['order', 'status']
    ordering = ['order', 'created_at']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'subtitle', 'block_type', 'status', 'order')
        }),
        ('Contenu textuel', {
            'fields': ('content',)
        }),
        ('Image', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Document', {
            'fields': ('document', 'document_title'),
            'classes': ('collapse',),
            'description': 'Upload de fichiers PDF, Word, Excel, PowerPoint, etc.'
        }),
        ('Vidéo', {
            'fields': (
                'video_type', 
                'video_file', 
                'video_url', 
                'video_embed_code', 
                'video_thumbnail'
            ),
            'classes': ('collapse',),
            'description': 'Vidéos locales, YouTube, Vimeo ou code d\'intégration'
        }),
        ('Lien optionnel', {
            'fields': ('link_url', 'link_text'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_media(self, obj):
        """Prévisualisation du média principal"""
        html = []
        
        if obj.image:
            html.append(format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px; margin-right: 5px;" title="Image"/>',
                obj.image.url
            ))
        
        if obj.document:
            ext = obj.get_document_extension()
            html.append(format_html(
                '<span style="background: #007cba; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; margin-right: 5px;" title="Document {}">{}</span>',
                obj.get_document_name(),
                ext
            ))
        
        if obj.video_file or obj.video_url or obj.video_embed_code:
            html.append(format_html(
                '<span style="background: #dc3545; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; margin-right: 5px;" title="Vidéo">📹</span>'
            ))
        
        return mark_safe(''.join(html)) if html else "Aucun média"
    preview_media.short_description = "Médias"
    
    def has_document(self, obj):
        """Indique si le bloc a un document"""
        if obj.document:
            return format_html(
                '<span style="color: green; font-weight: bold;" title="{}">✓ {}</span>',
                obj.get_document_name(),
                obj.get_document_extension()
            )
        return format_html('<span style="color: #ccc;">—</span>')
    has_document.short_description = "Document"
    
    def has_video(self, obj):
        """Indique si le bloc a une vidéo"""
        if obj.video_file:
            return format_html('<span style="color: green; font-weight: bold;" title="Vidéo locale">📹 Local</span>')
        elif obj.video_url:
            video_type = "YouTube" if "youtube" in obj.video_url or "youtu.be" in obj.video_url else "Vimeo" if "vimeo" in obj.video_url else "Externe"
            return format_html('<span style="color: blue; font-weight: bold;" title="{}">📹 {}</span>', obj.video_url, video_type)
        elif obj.video_embed_code:
            return format_html('<span style="color: purple; font-weight: bold;">📹 Embed</span>')
        return format_html('<span style="color: #ccc;">—</span>')
    has_video.short_description = "Vidéo"
    
    class Media:
        css = {
            'all': (
                'admin/css/pageblock_admin.css',
            )
        }
        js = (
            'admin/js/pageblock_admin.js',
        )

# CSS personnalisé pour l'admin
ADMIN_CSS = """
/* static/admin/css/pageblock_admin.css */
.field-preview_media img {
    border: 1px solid #ddd;
}

.fieldset.collapse .collapse-toggle {
    color: #007cba;
    font-weight: bold;
}

.field-video_type select {
    margin-bottom: 10px;
}

.field-document input[type="file"],
.field-video_file input[type="file"] {
    margin-bottom: 5px;
}

.help {
    font-size: 11px;
    color: #666;
    margin-top: 2px;
}

/* Style pour les types de fichiers */
.file-type-pdf { background-color: #dc3545; }
.file-type-doc, .file-type-docx { background-color: #007cba; }
.file-type-xls, .file-type-xlsx { background-color: #28a745; }
.file-type-ppt, .file-type-pptx { background-color: #fd7e14; }
"""

# JavaScript pour l'admin
ADMIN_JS = """
/* static/admin/js/pageblock_admin.js */
document.addEventListener('DOMContentLoaded', function() {
    // Gestion conditionelle des champs vidéo
    const videoTypeField = document.querySelector('#id_video_type');
    const videoFileField = document.querySelector('.field-video_file');
    const videoUrlField = document.querySelector('.field-video_url');
    const videoEmbedField = document.querySelector('.field-video_embed_code');
    
    function toggleVideoFields() {
        if (!videoTypeField) return;
        
        const selectedType = videoTypeField.value;
        
        // Masquer tous les champs
        if (videoFileField) videoFileField.style.display = 'none';
        if (videoUrlField) videoUrlField.style.display = 'none';
        if (videoEmbedField) videoEmbedField.style.display = 'none';
        
        // Afficher le champ approprié
        switch(selectedType) {
            case 'local':
                if (videoFileField) videoFileField.style.display = 'block';
                break;
            case 'youtube':
            case 'vimeo':
                if (videoUrlField) videoUrlField.style.display = 'block';
                break;
            case 'embed':
                if (videoEmbedField) videoEmbedField.style.display = 'block';
                break;
        }
    }
    
    if (videoTypeField) {
        videoTypeField.addEventListener('change', toggleVideoFields);
        toggleVideoFields(); // Exécuter au chargement
    }
    
    // Validation des URLs YouTube/Vimeo
    const videoUrlInput = document.querySelector('#id_video_url');
    if (videoUrlInput) {
        videoUrlInput.addEventListener('blur', function() {
            const url = this.value;
            if (url && !url.includes('youtube.com') && !url.includes('youtu.be') && !url.includes('vimeo.com')) {
                alert('Attention: Cette URL ne semble pas être une URL YouTube ou Vimeo valide.');
            }
        });
    }
});
"""