from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from .models import Post, Category, Comment, Project, Event, Course

# ============================================
# HOME & MAIN PAGES
# ============================================

def home_view(request):
    # Récupérer les derniers articles pour la page d'accueil
    recent_posts = Post.objects.filter(status='published')[:3]
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now())[:3]
    
    return render(request, 'pages/home.html', {
        'recent_posts': recent_posts,
        'featured_projects': featured_projects,
        'upcoming_events': upcoming_events,
    })

def about_view(request):
    return render(request, 'pages/about-us.html')

def contact_view(request):
    if request.method == 'POST':
        # Traiter le formulaire de contact
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # TODO: Envoyer email ou sauvegarder
        messages.success(request, 'Votre message a été envoyé avec succès!')
        return redirect('pages:contact')
    return render(request, 'pages/contact.html')

def gallery_view(request):
    projects = Project.objects.all()[:12]
    return render(request, 'pages/gallery.html', {'projects': projects})

def prices_view(request):
    return render(request, 'pages/pension-page.html')

def page_404_view(request, exception=None):
    return render(request, 'pages/404.html', status=404)

# ============================================
# BLOG
# ============================================

def blog_view(request):
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')
    
    posts = Post.objects.filter(status='published').order_by('-published_at')
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    paginator = Paginator(posts, 4)  # 4 articles par page
    page_obj = paginator.get_page(request.GET.get('page'))
    
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-published_at')[:3]
    
    return render(request, 'pages/blog.html', {
        'posts': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
    })

def blog_detail_view(request, slug):
    from .forms import CommentForm
    
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Incrémenter les vues
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Traiter les commentaires
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Votre commentaire a été soumis et sera publié après modération.')
            return redirect('pages:blog_detail', slug=slug)
        else:
            messages.error(request, 'Erreur dans le formulaire. Veuillez corriger les champs.')
    else:
        form = CommentForm()
    
    # Articles similaires
    related_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    # Commentaires approuvés
    comments = post.comments.filter(is_approved=True)
    
    return render(request, 'pages/standard_post.html', {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'comment_form': form,
    })

# ============================================
# PORTFOLIO
# ============================================

def portfolio_view(request):
    category_slug = request.GET.get('category', '')
    
    projects = Project.objects.all()
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    categories = Category.objects.filter(projects__isnull=False).distinct()
    
    return render(request, 'pages/portfolio.html', {
        'projects': projects,
        'categories': categories,
        'current_category': category_slug,
    })

def portfolio_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(id=project.id)[:3]
    
    return render(request, 'pages/portfolio-detail.html', {
        'project': project,
        'related_projects': related_projects,
    })

# ============================================
# EVENTS
# ============================================

def event_calendar_view(request):
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now())
    past_events = Event.objects.filter(start_date__lt=timezone.now())[:10]
    
    return render(request, 'pages/event-calendar.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'pages/event-detail.html', {'event': event})

# ============================================
# COURSES
# ============================================

# pages/views.py

def courses_view(request):
    """Liste des cours classés par filière"""
    from academique.models import Filiere
    
    # Récupérer les filières actives avec leurs cours
    filieres = Filiere.objects.filter(statut='active').prefetch_related('courses').order_by('nom')
    
    # Filtrer si recherche
    search = request.GET.get('search', '')
    if search:
        filieres = filieres.filter(
            Q(nom__icontains=search) | 
            Q(code__icontains=search)
        ).distinct()
    
    context = {
        'filieres': filieres,
        'search': search,
    }
    
    return render(request, 'pages/courses.html', context)

def course_detail_view(request, slug):
    """Détail d'un cours"""
    course = get_object_or_404(Course, slug=slug)
    
    # Cours similaires de la même filière
    related_courses = Course.objects.filter(
        filiere=course.filiere
    ).exclude(id=course.id)[:3] if course.filiere else Course.objects.exclude(id=course.id)[:3]
    
    return render(request, 'pages/course-detail.html', {
        'course': course,
        'related_courses': related_courses,
    })

# ============================================
# AUTRES PAGES (à développer)
# ============================================

def apply_view(request):
    return render(request, 'pages/apply.html')

def campus_tour_view(request):
    return render(request, 'pages/campus-tour.html')

# Academics
def business_administration_view(request):
    return render(request, 'pages/academics/business-administration.html')

def school_of_law_view(request):
    return render(request, 'pages/academics/school-of-law.html')

def engineering_view(request):
    return render(request, 'pages/academics/engineering.html')

def medicine_view(request):
    return render(request, 'pages/academics/medicine.html')

def art_science_view(request):
    return render(request, 'pages/academics/art-science.html')

def hospitality_management_view(request):
    return render(request, 'pages/academics/hospitality-management.html')

def physics_view(request):
    return render(request, 'pages/academics/physics.html')

def finance_view(request):
    return render(request, 'pages/academics/finance.html')

def finance_faculty_view(request):
    return render(request, 'pages/academics/finance-faculty.html')

def faculty_view(request):
    return render(request, 'pages/faculty.html')

def faculty_detail_view(request, faculty_id):
    return render(request, 'pages/faculty-detail.html', {'faculty_id': faculty_id})

def departments_view(request):
    return render(request, 'pages/departments.html')

def department_detail_view(request, dept_id):
    return render(request, 'pages/department-detail.html', {'dept_id': dept_id})

def cycles_view(request):
    return render(request, 'pages/cycles.html')

def cycle_detail_view(request, cycle_id):
    return render(request, 'pages/cycle-detail.html', {'cycle_id': cycle_id})

def resources_view(request):
    return render(request, 'pages/resources.html')

def resource_detail_view(request, resource_id):
    return render(request, 'pages/resource-detail.html', {'resource_id': resource_id})