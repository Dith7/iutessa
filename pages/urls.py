from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # ============================================
    # HOME & MAIN PAGES
    # ============================================
    path('', views.home_view, name='home'),
    path('about-us/', views.about_view, name='about-us'),
    path('contact/', views.contact_view, name='contact'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('prices/', views.prices_view, name='prices'),
    path('404/', views.page_404_view, name='404'),
    
    # ============================================
    # BLOG & POSTS
    # ============================================
    path('blog/', views.blog_view, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail_view, name='blog_detail'),
    path('posts/<int:post_id>/', views.blog_detail_view, name='post_detail'),
    
    # ============================================
    # PORTFOLIO
    # ============================================
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('portfolio/<int:project_id>/', views.portfolio_detail_view, name='portfolio_detail'),
    
    # ============================================
    # ADMISSIONS
    # ============================================
    path('apply/', views.apply_view, name='apply'),
    path('campus-tour/', views.campus_tour_view, name='campus-tour'),
    path('event-calendar/', views.event_calendar_view, name='event-calendar'),
    path('events/', views.event_calendar_view, name='events'),
    path('events/<int:event_id>/', views.event_detail_view, name='event_detail'),
    
    # ============================================
    # COURSES
    # ============================================
    path('courses/', views.courses_view, name='courses'),
    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail'),
    
    # ============================================
    # ACADEMICS - UNDERGRADUATE
    # ============================================
    path('academics/business-administration/', views.business_administration_view, name='business-administration'),
    path('academics/school-of-law/', views.school_of_law_view, name='school-of-law'),
    path('academics/engineering/', views.engineering_view, name='engineering'),
    path('academics/medicine/', views.medicine_view, name='medicine'),
    path('academics/art-science/', views.art_science_view, name='art-science'),
    
    # ============================================
    # ACADEMICS - GRADUATE
    # ============================================
    path('academics/hospitality-management/', views.hospitality_management_view, name='hospitality-management'),
    path('academics/physics/', views.physics_view, name='physics'),
    
    # ============================================
    # ACADEMICS - RESOURCES & FACULTY
    # ============================================
    path('academics/finance/', views.finance_view, name='finance'),
    path('academics/finance-faculty/', views.finance_faculty_view, name='finance-faculty'),
    path('faculty/', views.faculty_view, name='faculty'),
    path('faculty/<int:faculty_id>/', views.faculty_detail_view, name='faculty_detail'),
    
    # ============================================
    # DEPARTMENTS & CYCLES
    # ============================================
    path('departments/', views.departments_view, name='departments'),
    path('departments/<int:dept_id>/', views.department_detail_view, name='department_detail'),
    path('cycles/', views.cycles_view, name='cycles'),
    path('cycles/<int:cycle_id>/', views.cycle_detail_view, name='cycle_detail'),
    
    # ============================================
    # RESOURCES
    # ============================================
    path('ressources/', views.resources_view, name='ressources'),
    path('ressources/<int:resource_id>/', views.resource_detail_view, name='ressource_detail'),
]