"""
Django settings for opentrafficweb project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from configparser import RawConfigParser
#mz ++
from django.urls import reverse_lazy


config = RawConfigParser()
config['DEFAULT'] = {'SQLITE': ''}   # '' (~False) --or-- True
config.read('/etc/django/opentrafficweb/env.ini')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # probably same with/without abspath
# PROJECT_ROOT = PROJECT_DIR   # (this is shopon project style)
BASE_DIR = os.path.dirname(PROJECT_DIR)
DEV_TMP_DIR = os.path.join(BASE_DIR, '.devtmp')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.messages',

    'users',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    'django_extensions',

    'pokus',
    'django_b2',
    'pg_dump_anonymized',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'opentrafficweb.urls'

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

# django-allauth and related #mz ++ (from shopon)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends', 'user_location', 'user_likes'],
        # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
    },
    'google':
        {
            'SCOPE': ['profile', 'email'],
            'AUTH_PARAMS': {'access_type': 'online'}
        }
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_LOGOUT_ON_GET = True
# ACCOUNT_ADAPTER = 'mum.auth.adapter.AccountAdapter'
# ACCOUNT_SIGNUP_FORM_CLASS = 'mum.auth.forms.SignupForm'

LOGIN_REDIRECT_URL = reverse_lazy('index')

AUTH_USER_MODEL = 'users.User'

SITE_ID = 1
#mz ++ end


WSGI_APPLICATION = 'opentrafficweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

dbname = __package__.rsplit('.')[-2]
# postgres: missing or SQLITE=   ; sqlite: SQLITE=True, Yes, atp.
if os.environ.get('MZ_SQLITE') or bool(config.get('main', 'SQLITE')):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '%s.sqlite3' % dbname),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'ATOMIC_REQUESTS': True,
            'CONN_MAX_AGE': 1800,
            'HOST': 'localhost',  # ne '', kvůli např. reset_db
            'PORT': 5432,
            'NAME': dbname,
            'USER': dbname,
            'PASSWORD': os.environ.get('MZ_DB_PASSWORD') or config.get('main', 'DB_PASSWORD'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media and static settings, development
# https://docs.djangoproject.com/en/3.0/howto/static-files/ (+ shopon project ideas)
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(DEV_TMP_DIR, 'static')
STATIC_URL = '/static/'

# (shopon style, project level static/)
#STATICFILES_DIRS = [
#    os.path.join(PROJECT_DIR, 'static'),
#]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_ROOT = os.path.join(DEV_TMP_DIR, 'static', 'root')

MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = os.path.join(DEV_TMP_DIR, 'media')
#DEFAULT_FILE_STORAGE = 'b2_storage.storage.B2Storage'  # github.com/royendgel/django-backblazeb2-storage
DEFAULT_FILE_STORAGE = 'django_b2.storage.B2Storage'    # github.com/pyutil/django-b2 (using b2sdk, by zvolsky)
B2_APP_KEY_ID = os.environ.get('B2_APP_KEY_ID') or config.get('b2', 'B2_APP_KEY_ID')
B2_APP_KEY = os.environ.get('B2_APP_KEY') or config.get('b2', 'B2_APP_KEY')
B2_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME') or config.get('b2', 'B2_BUCKET_NAME')
B2_LOCAL_MEDIA = "ML"  # write media locally (M) and write log (L)
# unused from django-backblazeb2-storage, royendgel/ or other forks: BACKBLAZEB2_(same-as-B2-above) + ..:
#BACKBLAZEB2_ACCOUNT_ID = '000exxxxxxxxxxx000000000n'
#BACKBLAZEB2_BUCKET_ID = 'xxxxxxxxxxxxxxxxxxxxxxxx'
#BACKBLAZEB2_MAX_RETRIES = 3
#BACKBLAZEB2_BUCKET_PRIVATE = False


# colorlog + https://gist.github.com/raphaelyancey/bf8b53a2dbf675f9c99cf39f9e52c224
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',  # colored output

            # --> %(log_color)s is very important, that's what colors the line
            'format': '%(log_color)s[%(levelname)s] %(asctime)s :: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/opentrafficweb/django.log',   # changed !!!!!!!!
            'formatter': 'colored',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
