"""
Django settings for iconopedia project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os

from datetime import timedelta
from pathlib import Path


# Define exceptions for handling environment variable errors
class MissingEnvironmentVariable(Exception):
    """
    Exception to be raised when an environment variable is not defined.
    """
    def __init__(self, variable):
        """
        Initialization method called at exception creation. Here, the error message is defined.
        """
        super().__init__(f'Environment variable {variable} is not defined.')


class InvalidEnvironmentVariable(Exception):
    """
    Exception to be raised when the value of an environment variable is invalid.
    """
    def __init__(self, variable):
        """
        Initialization method called at exception creation. Here, the error message is defined.
        """
        super().__init__(
            f'The value of environment variable {variable} is not valid.')


# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['SECRET_KEY']
    STAGE = os.environ['STAGE']

    ADMIN_DATABASE_NAME = os.environ['ADMIN_DATABASE_NAME']
    ADMIN_DATABASE_USER = os.environ['ADMIN_DATABASE_USER']
    ADMIN_DATABASE_PASSWORD = os.environ['ADMIN_DATABASE_PASSWORD']

    DEFAULT_DATABASE_NAME = os.environ['DEFAULT_DATABASE_NAME']
    DEFAULT_DATABASE_USER = os.environ['DEFAULT_DATABASE_USER']
    DEFAULT_DATABASE_PASSWORD = os.environ['DEFAULT_DATABASE_PASSWORD']

    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

    MW_DICTIONARY_API_KEY = os.environ['MW_DICTIONARY_API_KEY']
except KeyError as exc:
    raise MissingEnvironmentVariable(exc)

VERSION = 'v0-alpha'

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Validate production stage environment variable

# SECURITY WARNING: don't run with debug turned on in production!
if STAGE == 'development' or STAGE == 'staging':
    DEBUG = True
elif STAGE == 'beta' or STAGE == 'production':
    DEBUG = False
else:
    raise InvalidEnvironmentVariable('STAGE')

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'api',
    'api.authentication',
    'api.dictionary',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_smtp_ssl',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iconopedia.urls'

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

WSGI_APPLICATION = 'iconopedia.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DEFAULT_DATABASE_NAME,
        'USER': DEFAULT_DATABASE_USER,
        'PASSWORD': DEFAULT_DATABASE_PASSWORD,
        'HOST': '',
        'PORT': '',
        'TEST': {
            'DEPENDENCIES': ['admin_db'],
        },
    },
    'admin_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ADMIN_DATABASE_NAME,
        'USER': ADMIN_DATABASE_USER,
        'PASSWORD': ADMIN_DATABASE_PASSWORD,
        'HOST': '',
        'PORT': '',
        'TEST': {
            'DEPENDENCIES': [],
        },
    },
}
DATABASE_ROUTERS = ['api.authentication.routers.AdminDBRouter']

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME':
        'api.authentication.password_validation.ContainsUppercaseValidator',
    },
    {
        'NAME':
        'api.authentication.password_validation.ContainsLowercaseValidator',
    },
    {
        'NAME':
        'api.authentication.password_validation.ContainsNumberValidator',
    },
    {
        'NAME':
        'api.authentication.password_validation.ContainsPunctuationValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Django REST Framework

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY':
    'errors',
    'DEFAULT_AUTHENTICATION_CLASSES':
    ['rest_framework_simplejwt.authentication.JWTAuthentication'],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    }
}

# Custom user model

AUTH_USER_MODEL = 'authentication.User'

# Email

DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

# Site ID

SITE_ID = 1

# Regular expression defining access and refresh tokens

TOKEN_REGEX = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$'

# Define default auto field to account for BigAutoField support added in 3.2

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF Simple JWT

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Changed from default
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,  # Changed from default
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer', ),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', ),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),  # Changed from default
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Default, front end paths for verification pages sent by email

FRONT_END_VERIFY_PATHS = {
    'REGISTER': '/register/verify',
    'PASSWORD_FORGOT': '/password/forgot/verify',
}

# Pagination

DEFAULT_RESULTS_PER_PAGE = 20
MAX_RESULTS_PER_PAGE = 100

# Count API calls (used in testing)
COUNT_API_CALLS = False
