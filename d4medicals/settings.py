"""
Django settings for d4medicals project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from os import getenv, path
import os
import sys
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import dotenv
import dj_database_url
from django.db import connections
from django.db.utils import OperationalError
from .DEFAULTS import DEFAULT_HEADERS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = BASE_DIR / ".env.local"

if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DEVELOPMENT_MODE = getenv('DEVELOPMENT_MODE', 'False') == 'True'



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ['127.0.0.1','localhost','https://d4-medicals.vercel.app' ,'d4medicalsserver.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',   
    'django.contrib.sessions',
    'django.contrib.messages',   
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'djoser',
    'social_django',
    'users',
    'events',
    'center',
    'bookings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'd4medicals.urls'

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

WSGI_APPLICATION = 'd4medicals.wsgi.application'

# Database   
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {}
try:
    if DEVELOPMENT_MODE is True:
        DATABASES = {
        "default" : {
            "ENGINE": "django.db.backends.postgresql",
            "NAME":  getenv("DB"),
            "USER": getenv("DB_USER"),
            "PASSWORD": getenv("DB_PASSWORD"),
            "HOST": getenv("DB_HOST"),
            "PORT": getenv("DB_PORT")   
         }
        }
    elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
        if getenv('DATABASE_URL', None) is None:
            raise Exception('DATABASE_URL environment variable not defined')
        DATABASES = {
            'default': dj_database_url.parse(getenv('DATABASE_URL')),
        }
    # Attempt to connect to the default database
    db_conn = connections['default']
    db_conn.cursor()  # This will attempt to establish a connection to the database

    print("Database connection successful!")   

except OperationalError as e:
    print("Database connection failed:", e)
except Exception as ex:
    print("An error occurred during database configuration:", ex)     


# Email settings

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = getenv("SENDGRID_API_KEY", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = getenv("SENDGRID_SENDER", "")  
DEFAULT_FROM_EMAIL = getenv('SENDGRID_SENDER')  

PROTOCOL = "http"
 
DOMAIN = getenv('DOMAIN')
SITE_NAME = 'D4 Medicals'    



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.facebook.FacebookOAuth2',   
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': True,
    # 'ACTIVATION_URL': 'activation/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,   
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [getenv('REDIRECT_URLS')]
}

AUTH_COOKIE = 'access'
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24
AUTH_COOKIE_SECURE = getenv('AUTH_COOKIE_SECURE') #getenv('AUTH_COOKIE_SECURE', 'True') == 'True'
AUTH_COOKIE_HTTP_ONLY = getenv('AUTH_COOKIE_HTTP_ONLY') #True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'None'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv('GOOGLE_AUTH_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = getenv('GOOGLE_AUTH_SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',  
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']



LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'NOTSET',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR'
        }
    }
}



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field



CORS_ALLOWED_ORIGINS = [  
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://d4-medicals.vercel.app'  
    
]

CSRF_TRUSTED_ORIGINS = [     
    'http://localhost:3000',
    'http://127.0.0.1:3000',  
    'https://d4-medicals.vercel.app'
]

# CORS_ORIGIN_ALLOW_ALL=True
# CORS_ALLOW_ALL_ORIGINS=True


CORS_ALLOW_CREDENTIALS = True
  
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = DEFAULT_HEADERS 
  
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.UserAccount'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'