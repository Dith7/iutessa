# 🎓 Plateforme Université - Documentation Complète

## Vue d'ensemble

**Plateforme Université** est un CMS Django pour universités avec gestion de blocs de contenu dynamiques. Supporte texte, images, documents (PDF, Word, Excel) et vidéos (locales, YouTube, Vimeo).

### Technologies
- **Backend** : Django 5.2+, CKEditor 5
- **Frontend** : Tailwind CSS 3.8+
- **DB** : SQLite (dev), PostgreSQL/MySQL (prod)
- **Médias** : Pillow, validation fichiers

## Architecture technique

### Structure du projet
```
iuttessa/
├── manage.py
├── requirements.txt
├── README.md
├── votre_projet/                    # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pages/                          # Application principale
│   ├── models.py                   # Modèle PageBlock
│   ├── admin.py                    # Interface admin
│   ├── views.py                    # Vues Django
│   ├── urls.py
│   ├── migrations/
│   └── management/commands/
│       └── create_default_blocks.py
├── templates/                      # Templates globaux
│   ├── base.html
│   └── pages/                      # Templates pages
│       ├── home.html
│       ├── blocks/                 # Templates de blocs
│       │   ├── hero.html
│       │   ├── about.html
│       │   ├── contact.html
│       │   ├── news.html
│       │   ├── gallery.html
│       │   ├── services.html
│       │   ├── documents.html
│       │   ├── videos.html
│       │   ├── testimonials.html
│       │   ├── stats.html
│       │   ├── team.html
│       │   ├── custom.html
│       │   └── default.html
│       └── partials/               # Templates partiels
│           ├── document.html
│           ├── video.html
│           └── media_gallery.html
├── static/                         # Fichiers statiques
│   ├── admin/css/
│   ├── admin/js/
│   └── pages/
├── media/                          # Fichiers uploadés
│   ├── blocks/images/
│   ├── documents/
│   ├── videos/
│   └── videos/thumbnails/
└── theme/                          # Tailwind CSS
```

### Modèle PageBlock

**Champs principaux :**
- `title`, `subtitle` : Titre et sous-titre
- `content` : Contenu riche (CKEditor 5)
- `block_type` : Type de bloc (hero, about, contact, etc.)
- `order` : Ordre d'affichage
- `status` : actif/inactif

**Médias :**
- `image` : Image principale
- `document` : PDF, Word, Excel, PowerPoint
- `document_title` : Titre personnalisé
- `video_type` : local, YouTube, Vimeo, embed
- `video_file`, `video_url`, `video_embed_code`
- `video_thumbnail` : Miniature

**Types de blocs :**
hero, about, contact, news, gallery, documents, videos, services, testimonials, stats, team, custom

## Installation

### Prérequis
- Python 3.10+
- Node.js 16+ (pour Tailwind)
- Git

### Installation rapide
```bash
# 1. Environnement
git clone [URL_DEPOT]
cd iuttessa
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 2. Configuration
cp votre_projet/settings.py.example votre_projet/settings.py
# Éditer SECRET_KEY, DEBUG, ALLOWED_HOSTS

# 3. Base de données
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 4. Tailwind CSS
python manage.py tailwind init
python manage.py tailwind install

# 5. Données par défaut
python manage.py create_default_blocks

# 6. Démarrage
# Terminal 1:
python manage.py runserver
# Terminal 2:
python manage.py tailwind start
```

### Configuration production
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iuttessa_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'
```

## Utilisation

### Interface admin
1. Accès : `http://localhost:8000/admin/`
2. **Blocs de page** → **Ajouter** nouveau bloc
3. Champs obligatoires : Titre, Type de bloc, Ordre
4. **Médias** : Image, Document, Vidéo (optionnels)
5. **Statut** : Actif pour afficher

### Types de médias supportés
- **Documents** : PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT (max 50MB)
- **Vidéos locales** : MP4, WebM, AVI, MOV (max 50MB)
- **Vidéos externes** : URLs YouTube, Vimeo
- **Embed** : Code iframe personnalisé

### Bonnes pratiques
- **Ordre logique** : Hero (1) → About (2) → Services (3) → Contact (4)
- **Images optimisées** : 1920px max width, format WebP recommandé
- **Documents** : Noms descriptifs, taille raisonnable
- **Vidéos** : MP4 H.264 pour compatibilité maximale

## Développement

### Créer nouveau type de bloc
```python
# 1. pages/models.py
BLOCK_TYPES = [
    # ... existants
    ('nouveau_type', 'Nouveau Type'),
]

# 2. templates/pages/blocks/nouveau_type.html
<div class="py-16 bg-white">
    <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold mb-6">{{ block.title }}</h2>
        {{ block.content|safe }}
    </div>
</div>

# 3. Migration
python manage.py makemigrations pages
python manage.py migrate
```

### Variables templates disponibles
```html
{{ block.title }}               <!-- Titre -->
{{ block.subtitle }}            <!-- Sous-titre -->
{{ block.content|safe }}        <!-- Contenu riche -->
{{ block.image.url }}           <!-- URL image -->
{{ block.document.url }}        <!-- URL document -->
{{ block.get_document_name }}   <!-- Nom document -->
{{ block.get_document_size }}   <!-- Taille document -->
{{ block.get_video_embed_url }} <!-- URL embed vidéo -->
{{ block.has_media }}           <!-- Booléen médias -->
```

### Templates partiels
```html
<!-- Galerie complète -->
{% include 'pages/partials/media_gallery.html' with block=block %}

<!-- Document seul -->
{% include 'pages/partials/document.html' with block=block %}

<!-- Vidéo seule -->
{% include 'pages/partials/video.html' with block=block %}
```

## Maintenance

### Sauvegardes
```bash
# Backup données
python manage.py dumpdata > backup_$(date +%Y%m%d).json
python manage.py dumpdata pages.PageBlock > backup_blocks.json

# Backup médias
tar -czf media_backup.tar.gz media/

# Restauration
python manage.py loaddata backup_20250814.json
```

### Mises à jour
```bash
# 1. Backup avant mise à jour
python manage.py dumpdata > backup_before_update.json

# 2. Pull code
git pull origin main

# 3. Dépendances
pip install -r requirements.txt

# 4. Migrations
python manage.py migrate

# 5. Static files
python manage.py collectstatic --noinput

# 6. Restart serveur
```

### Monitoring
```python
# settings.py - Logs
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

## Résolution de problèmes

### Erreurs communes

**TemplateDoesNotExist**
```bash
# Créer template manquant
mkdir -p templates/pages/blocks/
cp templates/pages/blocks/default.html templates/pages/blocks/[TYPE_MANQUANT].html
```

**Permission denied sur media/**
```bash
chmod -R 755 media/
chown -R www-data:www-data media/  # Production
```

**CKEditor ne charge pas**
```python
# urls.py - Vérifier inclusion
path("ckeditor5/", include('django_ckeditor_5.urls')),
```

**Tailwind CSS ne fonctionne pas**
```bash
# Réinstaller
python manage.py tailwind install
python manage.py tailwind build
```

### Debug
```bash
# Mode debug
python manage.py runserver --settings=votre_projet.settings_debug

# Shell Django
python manage.py shell
>>> from pages.models import PageBlock
>>> PageBlock.objects.all()

# Vérifications
python manage.py check
python manage.py check --deploy
```

## Prise en main nouveau développeur

### Setup rapide (30 min)
```bash
# 1. Installation (10 min)
git clone [REPO_URL] && cd iuttessa
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate && python manage.py createsuperuser
python manage.py create_default_blocks --with-media-examples

# 2. Exploration (10 min)
python manage.py runserver
# Visiter http://localhost:8000/admin/ et http://localhost:8000/

# 3. Premier développement (10 min)
# Modifier un template dans templates/pages/blocks/
# Créer un nouveau type de bloc
# Tester upload document/vidéo
```

### Points clés
- **Modèle central** : PageBlock dans pages/models.py
- **Templates** : Un par type dans templates/pages/blocks/
- **Admin** : Interface principale pour contenu
- **Tailwind** : Tous les styles
- **Médias** : Support complet docs/vidéos

## Commandes de référence

### Django
```bash
# Base
python manage.py runserver [port]
python manage.py shell
python manage.py makemigrations [app]
python manage.py migrate
python manage.py createsuperuser

# Données
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
python manage.py create_default_blocks [--with-media-examples]

# Production
python manage.py collectstatic --noinput
python manage.py check --deploy
```

### Tailwind
```bash
python manage.py tailwind init
python manage.py tailwind install
python manage.py tailwind start    # Développement
python manage.py tailwind build    # Production
```

### Git workflow
```bash
git checkout -b feature/nouvelle-fonctionnalite
git add . && git commit -m "feat: description"
git push origin feature/nouvelle-fonctionnalite
# Merge request → main
```

## Roadmap

### Modules prévus
1. **Gestion utilisateurs** - Rôles ADMIN/ETUDIANT/VISITEUR
2. **Inscriptions académiques** - Import Excel, génération PDF
3. **Gestion concours** - Candidatures, validation, résultats

### Améliorations possibles
- SEO avancé, cache, API REST
- Multi-langues, analytics, newsletter
- CMS avancé, e-learning, mobile app

## Support

### En cas de problème
1. **Logs** : `python manage.py runserver`
2. **Config** : `python manage.py check`
3. **Shell** : `python manage.py shell`
4. **Documentation** : Cette section

### Maintenance
- **Sécurité** : Immédiate
- **Dépendances** : Mensuelle
- **Features** : Selon roadmap

---

**Version** : 1.0.0  
**Dernière MAJ** : 14 août 2025  
**Statut** : Module Pages complet ✅