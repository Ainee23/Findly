"""
Django settings for Findly project.
"""

from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-_!n5wpf%!_v_a60$jm6-y$f))=la*f37v@ntxo0)c#k!7n)_so')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',

    'core',
    'accounts',
    'items',
    'messaging',
    'notifications',
    'reviews',
    'dashboard',
    'qr',
    'ai',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.ActiveUserMiddleware',
]

ROOT_URLCONF = 'Findly.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ✅ Notifications badge in navbar
                'notifications.context_processors.unread_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'Findly.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Findly',
        'USER': 'postgres',
        'PASSWORD': 'ainee123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # ✅ added
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Custom User Model (core app)
AUTH_USER_MODEL = 'core.User'

# Auth redirects — keeping core app behaviour
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = "findly@gmail.com"

# ================= EMAIL CONFIG =================
# To send real emails, uncomment these and add a valid app password
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'yourgmail@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_16_digit_app_password'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'