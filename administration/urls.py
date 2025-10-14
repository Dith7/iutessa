from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    # ============================================
    # DASHBOARD
    # ============================================
    path('', views.dashboard_view, name='dashboard'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('settings/', views.settings_view, name='settings'),
    
    # ============================================
    # ACADÉMIQUE
    # ============================================
    path('academic/', views.academic_overview, name='academic_overview'),
    path('documents/', views.documents_validation, name='documents_validation'),
    path('documents/<int:document_id>/validate/', views.validate_document, name='validate_document'),
    path('filieres/', views.filieres_management, name='filieres_management'),
    
    # ============================================
    # BLOG
    # ============================================
    path('blog/', views.blog_management, name='blog_management'),
    path('blog/nouveau/', views.blog_create, name='blog_create'),
    path('blog/<int:post_id>/modifier/', views.blog_edit, name='blog_edit'),
    path('blog/<int:post_id>/supprimer/', views.blog_delete, name='blog_delete'),
    
    # Commentaires
    path('blog/commentaires/', views.blog_comments, name='blog_comments'),
    path('blog/commentaires/<int:comment_id>/approuver/', views.comment_approve, name='comment_approve'),
    path('blog/commentaires/<int:comment_id>/supprimer/', views.comment_delete, name='comment_delete'),
    
    # ============================================
    # CATÉGORIES
    # ============================================
    path('categories/', views.categories_management, name='categories_management'),
    path('categories/<int:category_id>/supprimer/', views.category_delete, name='category_delete'),
    
    # ============================================
    # PORTFOLIO
    # ============================================
    path('portfolio/', views.portfolio_management, name='portfolio_management'),
    path('portfolio/nouveau/', views.portfolio_create, name='portfolio_create'),
    path('portfolio/<int:project_id>/modifier/', views.portfolio_edit, name='portfolio_edit'),
    path('portfolio/<int:project_id>/supprimer/', views.portfolio_delete, name='portfolio_delete'),


    # ============================================
    # courses
    # ============================================

    path('courses/', views.courses_management, name='courses_management'),
    path('courses/nouveau/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/modifier/', views.course_edit, name='course_edit'),
    path('courses/<int:course_id>/supprimer/', views.course_delete, name='course_delete'),
]