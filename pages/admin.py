from django.contrib import admin
from .models import Category, Post, PostImage, PostDocument, Comment, Project, Event, Course

# ============================================
# CATEGORY
# ============================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'posts_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'Nombre d\'articles'

# ============================================
# BLOG
# ============================================

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ['image', 'caption', 'order']

class PostDocumentInline(admin.TabularInline):
    model = PostDocument
    extra = 1
    fields = ['title', 'file', 'description', 'order']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'has_media', 'views_count', 'published_at', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [PostImageInline, PostDocumentInline]
    
    fieldsets = (
        ('Contenu principal', {
            'fields': ('title', 'slug', 'author', 'featured_image', 'excerpt', 'content')
        }),
        ('Médias', {
            'fields': ('video_url', 'video_file'),
            'description': 'Ajouter une vidéo YouTube/Vimeo (URL) ou uploader un fichier vidéo'
        }),
        ('Classification', {
            'fields': ('category', 'tags', 'status')
        }),
        ('Statistiques', {
            'fields': ('published_at', 'views_count'),
            'classes': ('collapse',)
        }),
    )
    
    def has_media(self, obj):
        """Icône indiquant si l'article a des médias"""
        media_count = 0
        if obj.featured_image:
            media_count += 1
        if obj.video_url or obj.video_file:
            media_count += 1
        media_count += obj.images.count()
        media_count += obj.documents.count()
        
        if media_count > 0:
            return f"✅ {media_count}"
        return "—"
    has_media.short_description = 'Médias'
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'image', 'caption', 'order']
    list_filter = ['post']
    search_fields = ['caption', 'post__title']
    list_editable = ['order']

@admin.register(PostDocument)
class PostDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'post', 'get_file_size', 'get_file_extension', 'order', 'uploaded_at']
    list_filter = ['post', 'uploaded_at']
    search_fields = ['title', 'description', 'post__title']
    list_editable = ['order']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'author_email', 'content']
    date_hierarchy = 'created_at'
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approuver les commentaires sélectionnés"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Désapprouver les commentaires sélectionnés"

# ============================================
# PORTFOLIO
# ============================================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'client', 'is_featured', 'order', 'created_at']
    list_filter = ['is_featured', 'category', 'created_at']
    search_fields = ['title', 'description', 'client']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'is_featured']
    ordering = ['order', '-created_at']

# ============================================
# EVENTS
# ============================================

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'start_date', 'end_date', 'is_featured']
    list_filter = ['is_featured', 'start_date']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    list_editable = ['is_featured']

# ============================================
# COURSES
# ============================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'duration', 'level', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['title', 'description', 'instructor']
    prepopulated_fields = {'slug': ('title',)}