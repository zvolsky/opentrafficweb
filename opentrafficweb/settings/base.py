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

    'common',
    'accounts',
    'users',
    'main',

    'compressor',
    'widget_tweaks',
    'django_extensions',

    'django_countries',
    'countries_plus',
    'languages_plus',
    'cities_light',

    'django_b2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'accounts:login'
# custom settings used in 'accounts' app
HOME_URL = 'admin:home'
LOGIN_REDIRECT_URL = HOME_URL
LOGOUT_REDIRECT_URL = HOME_URL


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
LOCALE_PATHS = ['locale']

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media and static settings, development
# https://docs.djangoproject.com/en/3.0/howto/static-files/ (+ shopon project ideas)
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(DEV_TMP_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',      # shromáždí ze STATICFILES_DIRS
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # shromáždí ze všech <app>/static/
    'compressor.finders.CompressorFinder',   # překlad sass
]

COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'django_libsass.SassCompiler'),
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_ROOT = os.path.join(DEV_TMP_DIR, 'static', 'root')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DEV_TMP_DIR, 'media')
DEFAULT_FILE_STORAGE = 'django_b2.storage.B2Storage'    # github.com/pyutil/django-b2 (using b2sdk, by zvolsky)
B2_APP_KEY_ID = os.environ.get('B2_APP_KEY_ID') or config.get('b2', 'B2_APP_KEY_ID')
B2_APP_KEY = os.environ.get('B2_APP_KEY') or config.get('b2', 'B2_APP_KEY')
B2_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME') or config.get('b2', 'B2_BUCKET_NAME')
B2_LOCAL_MEDIA = "ML"  # write media locally (M) and write log (L)

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
            'handlers': ['console'],  # ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}


# geoip2 / geolite2
GEOIP_PATH = "/var/lib/GeoIP/"   # podrobnosti k instalaci: keepasx: geolite2

# django-cities-light
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en', 'es', 'de', 'fr', 'cz', 'abbr']
