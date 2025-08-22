"""
Configuration Django complète avec CKEditor 5, Tailwind CSS et Google Cloud Storage
"""
import os
from pathlib import Path
from google.oauth2 import service_account
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ====================
# VARIABLES SECRÈTES
# ====================
SECRET_KEY = os.getenv("SECRET_KEY", "insecure-key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

AUTH_USER_MODEL = 'users.User'

# URLs de redirection
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:dashboard'
LOGOUT_REDIRECT_URL = 'pages:home'


# ====================
# APPLICATIONS
# ====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps tiers
    'tailwind',
    'theme',
    'django_ckeditor_5',
    'storages',

    # Vos apps
    'pages',
    'administration',
    'users',
    'academique',
    'notifications',
    # 'concours',   # à ajouter plus tard
]


# ====================
# GOOGLE CLOUD STORAGE
# ====================
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME")
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
)


# ====================
# MIDDLEWARE
# ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iuttessa.urls'

# ====================
# TEMPLATES
# ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

# ====================
# SÉCURITÉ
# ====================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ====================
# SESSIONS
# ====================
SESSION_COOKIE_AGE = 86400  # 24 heures
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

WSGI_APPLICATION = 'iuttessa.wsgi.application'

# ====================
# DATABASE
# ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ====================
# PASSWORD VALIDATORS
# ====================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ====================
# INTERNATIONALISATION
# ====================
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "fr-fr")
TIME_ZONE = os.getenv("TIME_ZONE", "Africa/Douala")
USE_I18N = True
USE_TZ = True

# ====================
# STATIC & MEDIA
# ====================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"
MEDIA_ROOT = ""

# ====================
# AUTO FIELD
# ====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====================
# CONFIGURATION TAILWIND
# ====================
TAILWIND_APP_NAME = 'theme'

if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
NPM_BIN_PATH = '/usr/bin/npm'
# NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'

# ====================
# CONFIGURATION CKEDITOR 5
# ====================

# Palette de couleurs personnalisée pour l'université
UNIVERSITY_COLOR_PALETTE = [
    {'color': '#1e40af', 'label': 'Bleu Université'},
    {'color': '#dc2626', 'label': 'Rouge Université'},
    {'color': '#059669', 'label': 'Vert Université'},
    {'color': '#d97706', 'label': 'Orange Université'},
    {'color': '#7c3aed', 'label': 'Violet Université'},
    {'color': '#374151', 'label': 'Gris Foncé'},
    {'color': '#6b7280', 'label': 'Gris'},
    {'color': '#f3f4f6', 'label': 'Gris Clair'},
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 
            'bold', 'italic', 'underline', '|',
            'link', 'bulletedList', 'numberedList', '|',
            'blockQuote', 'insertImage', '|',
            'undo', 'redo'
        ],
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraphe', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Titre 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Titre 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Titre 3', 'class': 'ck-heading_heading3'}
            ]
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight', '|',
                'imageStyle:full', 'imageStyle:side'
            ],
            'styles': ['full', 'side', 'alignLeft', 'alignRight', 'alignCenter']
        },
    },
    
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3', '|',
            'bulletedList', 'numberedList', '|',
            'blockQuote', 'insertTable'
        ],
        'toolbar': [
            'heading', '|',
            'outdent', 'indent', '|',
            'bold', 'italic', 'underline', 'strikethrough', 'code', '|',
            'subscript', 'superscript', 'highlight', '|',
            'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|',
            'link', 'insertImage', 'mediaEmbed', '|',
            'bulletedList', 'numberedList', 'todoList', '|',
            'blockQuote', 'codeBlock', 'insertTable', '|',
            'sourceEditing', 'removeFormat', '|',
            'undo', 'redo'
        ],
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraphe', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Titre 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Titre 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Titre 3', 'class': 'ck-heading_heading3'},
                {'model': 'heading4', 'view': 'h4', 'title': 'Titre 4', 'class': 'ck-heading_heading4'}
            ]
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight', '|',
                'imageStyle:full', 'imageStyle:side', '|',
                'linkImage'
            ],
            'styles': ['full', 'side', 'alignLeft', 'alignRight', 'alignCenter']
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells', '|',
                'tableProperties', 'tableCellProperties'
            ],
            'tableProperties': {
                'borderColors': UNIVERSITY_COLOR_PALETTE,
                'backgroundColors': UNIVERSITY_COLOR_PALETTE
            },
            'tableCellProperties': {
                'borderColors': UNIVERSITY_COLOR_PALETTE,
                'backgroundColors': UNIVERSITY_COLOR_PALETTE
            }
        },
        'fontColor': {
            'colors': [
                {'color': '#000000', 'label': 'Noir'},
                {'color': '#ffffff', 'label': 'Blanc'},
            ] + UNIVERSITY_COLOR_PALETTE
        },
        'fontBackgroundColor': {
            'colors': [
                {'color': '#000000', 'label': 'Noir'},
                {'color': '#ffffff', 'label': 'Blanc'},
            ] + UNIVERSITY_COLOR_PALETTE
        },
        'fontSize': {
            'options': ['tiny', 'small', 'default', 'big', 'huge']
        },
        'link': {
            'decorators': {
                'addTargetToExternalLinks': True,
                'defaultProtocol': 'https://',
            }
        },
        'list': {
            'properties': {
                'styles': True,
                'startIndex': True,
                'reversed': True,
            }
        }
    }
}

# Upload d'images pour CKEditor 5
CKEDITOR_5_UPLOAD_PATH = "uploads/"

# ====================
# LOGGING
# ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'pages': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# ====================
# EMAIL
# ====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

# Créer le dossier logs s'il n'existe pas
(BASE_DIR / 'logs').mkdir(exist_ok=True)
