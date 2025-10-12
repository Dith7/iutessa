from django.shortcuts import render

# ============================================
# HOME & MAIN PAGES
# ============================================

def home_view(request):
    return render(request, 'pages/home.html', {
        'title': 'IUTESSA Mokolo',
        'page_type': 'home'
    })

def about_view(request):
    return render(request, 'pages/about-us.html', {
        'title': 'À Propos d\'IUTESSA',
        'page_type': 'about'
    })

def contact_view(request):
    return render(request, 'pages/contact.html', {
        'title': 'Contact - IUTESSA',
        'page_type': 'contact'
    })

def gallery_view(request):
    return render(request, 'pages/gallery.html', {
        'title': 'Galerie - IUTESSA',
        'page_type': 'gallery'
    })

def prices_view(request):
    return render(request, 'pages/pension-page.html', {
        'title': 'Tarifs - IUTESSA',
        'page_type': 'prices'
    })

def page_404_view(request):
    return render(request, 'pages/404.html', {
        'title': 'Page Non Trouvée',
        'page_type': '404'
    })

# ============================================
# BLOG & POSTS
# ============================================

def blog_view(request):
    return render(request, 'pages/blog.html', {
        'title': 'Blog - IUTESSA',
        'page_type': 'blog'
    })

def blog_detail_view(request, post_id):
    return render(request, 'pages/standard_post.html', {
        'title': f'Article {post_id} - IUTESSA',
        'page_type': 'blog_detail',
        'post_id': post_id
    })

# ============================================
# PORTFOLIO
# ============================================

def portfolio_view(request):
    return render(request, 'pages/portfolio.html', {
        'title': 'Portfolio - IUTESSA',
        'page_type': 'portfolio'
    })

def portfolio_detail_view(request, project_id):
    return render(request, 'pages/porfolio.html', {
        'title': f'Projet {project_id} - IUTESSA',
        'page_type': 'portfolio_detail',
        'project_id': project_id
    })

# ============================================
# ADMISSIONS
# ============================================

def apply_view(request):
    return render(request, 'pages/apply-to-iutessa.html', {
        'title': 'Postuler à IUTESSA',
        'page_type': 'apply'
    })

def campus_tour_view(request):
    return render(request, 'pages/campus-tour.html', {
        'title': 'Visite du Campus - IUTESSA',
        'page_type': 'campus_tour'
    })

def event_calendar_view(request):
    return render(request, 'pages/event-calendar.html', {
        'title': 'Calendrier des Événements',
        'page_type': 'events'
    })

def event_detail_view(request, event_id):
    return render(request, 'pages/event-calendar.html', {
        'title': f'Événement {event_id} - IUTESSA',
        'page_type': 'event_detail',
        'event_id': event_id
    })

# ============================================
# COURSES
# ============================================

def courses_view(request):
    return render(request, 'pages/course-list.html', {
        'title': 'Formations - IUTESSA',
        'page_type': 'courses'
    })

def course_detail_view(request, course_id):
    return render(request, 'pages/course-list.html', {
        'title': f'Formation {course_id} - IUTESSA',
        'page_type': 'course_detail',
        'course_id': course_id
    })
    
    
    # ==================
    # From here nothign done yet we will have to go page by page 

# ============================================
# ACADEMICS - UNDERGRADUATE
# ============================================

def business_administration_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Administration des Affaires - IUTESSA',
        'page_type': 'business_admin'
    })

def school_of_law_view(request):
    return render(request, 'pages/home.html', {
        'title': 'École de Droit - IUTESSA',
        'page_type': 'law'
    })

def engineering_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Ingénierie - IUTESSA',
        'page_type': 'engineering'
    })

def medicine_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Médecine - IUTESSA',
        'page_type': 'medicine'
    })

def art_science_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Arts & Sciences - IUTESSA',
        'page_type': 'art_science'
    })

# ============================================
# ACADEMICS - GRADUATE
# ============================================

def hospitality_management_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Gestion Hôtelière - IUTESSA',
        'page_type': 'hospitality'
    })

def physics_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Physique - IUTESSA',
        'page_type': 'physics'
    })

# ============================================
# ACADEMICS - RESOURCES & FACULTY
# ============================================

def finance_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Finance - IUTESSA',
        'page_type': 'finance'
    })

def finance_faculty_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Corps Enseignant Finance - IUTESSA',
        'page_type': 'finance_faculty'
    })

def faculty_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Corps Enseignant - IUTESSA',
        'page_type': 'faculty'
    })

def faculty_detail_view(request, faculty_id):
    return render(request, 'pages/home.html', {
        'title': f'Enseignant {faculty_id} - IUTESSA',
        'page_type': 'faculty_detail',
        'faculty_id': faculty_id
    })

# ============================================
# DEPARTMENTS & CYCLES
# ============================================

def departments_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Départements - IUTESSA',
        'page_type': 'departments'
    })

def department_detail_view(request, dept_id):
    return render(request, 'pages/home.html', {
        'title': f'Département {dept_id} - IUTESSA',
        'page_type': 'department_detail',
        'dept_id': dept_id
    })

def cycles_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Cycles d\'Études - IUTESSA',
        'page_type': 'cycles'
    })

def cycle_detail_view(request, cycle_id):
    return render(request, 'pages/home.html', {
        'title': f'Cycle {cycle_id} - IUTESSA',
        'page_type': 'cycle_detail',
        'cycle_id': cycle_id
    })

# ============================================
# RESOURCES
# ============================================

def resources_view(request):
    return render(request, 'pages/home.html', {
        'title': 'Ressources - IUTESSA',
        'page_type': 'resources'
    })

def resource_detail_view(request, resource_id):
    return render(request, 'pages/home.html', {
        'title': f'Ressource {resource_id} - IUTESSA',
        'page_type': 'resource_detail',
        'resource_id': resource_id
    })