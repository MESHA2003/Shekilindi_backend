import os
from pathlib import Path
from datetime import timedelta

# =============================================================================
# BASE DIRECTORY
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECRET KEY & DEBUG
# =============================================================================
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-change-this-secret-key'
)

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# =============================================================================
# ALLOWED HOSTS (Render + local)
# =============================================================================
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',  # Allows *.onrender.com
]

# Dynamically add Render URL if available
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# =============================================================================
# INSTALLED APPS
# =============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    # Local apps
    'accounts',
    'clinic',
]

# =============================================================================
# MIDDLEWARE
# =============================================================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# ROOT URL CONFIGURATION
# =============================================================================
ROOT_URLCONF = 'backend.urls'

# =============================================================================
# TEMPLATES
# =============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# =============================================================================
# WSGI APPLICATION
# =============================================================================
WSGI_APPLICATION = 'backend.wsgi.application'

# =============================================================================
# DATABASE CONFIGURATION (PostgreSQL via DATABASE_URL for Render)
# =============================================================================
import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Production: Use DATABASE_URL from Render's environment variables
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback: Use the Render PostgreSQL database directly
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://herbal_clinic_db_user:NHD4bngmk3yfudQQ7yXmXTFIVPZ2zANr@dpg-d8akqk77f7vs73d8lr6g-a/herbal_clinic_db',
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# =============================================================================
# PASSWORD VALIDATORS
# =============================================================================
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

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# =============================================================================
# STATIC FILES
# =============================================================================
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================================================
# MEDIA FILES
# =============================================================================
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# DEFAULT PRIMARY KEY FIELD
# =============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================
AUTH_USER_MODEL = 'accounts.User'

# =============================================================================
# CORS SETTINGS
# =============================================================================
CORS_ALLOWED_ORIGINS = [
    # Frontend on Vercel (update this with your actual Vercel URL)
    "https://herbal-clinic-frontend.vercel.app",

    # Local development
    "http://localhost:3000",
    "http://localhost:5173",
]

# Allow all subdomains of your Vercel app
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://[a-zA-Z0-9-]+\.vercel\.app$",
]

CORS_ALLOW_CREDENTIALS = True

# Parse additional CORS origins from environment variable
CORS_ORIGINS_ENV = os.getenv('CORS_ALLOWED_ORIGINS')
if CORS_ORIGINS_ENV:
    extra_origins = [origin.strip() for origin in CORS_ORIGINS_ENV.split(',') if origin.strip()]
    CORS_ALLOWED_ORIGINS.extend(extra_origins)

# =============================================================================
# CSRF TRUSTED ORIGINS
# =============================================================================
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# Dynamically add Render URL if available
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# =============================================================================
# DJANGO REST FRAMEWORK
# =============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 10,
}

# =============================================================================
# SIMPLE JWT
# =============================================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),

    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ROTATE_REFRESH_TOKENS': True,

    'BLACKLIST_AFTER_ROTATION': True,
}

# =============================================================================
# SECURITY SETTINGS (Production)
# =============================================================================
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1', 't')

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

USE_X_FORWARDED_HOST = True