import os
from configparser import RawConfigParser

from .base import *

# TODO: fix ALLOWED_HOSTS
# jakým mechanismem běží mojeknihovna.eu - není v sites-enabled

config = RawConfigParser()
config['DEFAULT'] = {'ALLOWED_HOSTS': '*'}   # toto asi nechodí
config.read('/etc/django/opentrafficweb/env.ini')


DEBUG = False
SECRET_KEY = os.environ.get('MZ_SECRET_KEY') or config.get('main', 'SECRET_KEY')
# v ALLOWED_HOSTS musí být i www.<domena>, tj. např. <domena>,www.<domena>,*.<domena>
ALLOWED_HOSTS = (os.environ.get('MZ_ALLOWED_HOSTS') or config.get('main', 'ALLOWED_HOSTS')
                 ).replace(',', ' ').replace(';', ' ').split()

X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'same-origin'

try:
    from .local import *
except ImportError:
    pass

GEOIP_PATH = "/usr/share/GeoIP/"    # as long on older Debian (?)

LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'filters': {
    'require_debug_false': {
        '()': 'django.utils.log.RequireDebugFalse',
    },
    'require_debug_true': {
        '()': 'django.utils.log.RequireDebugTrue',
    },
},
'formatters': {
    'django.server': {
        '()': 'django.utils.log.ServerFormatter',
        'format': '[%(server_time)s] %(message)s',
    }
},
'handlers': {
    'console': {
        'level': 'INFO',
        'filters': ['require_debug_true'],
        'class': 'logging.StreamHandler',
    },
    # Custom handler which we will use with logger 'django'.
    # We want errors/warnings to be logged when DEBUG=False
    'console_on_not_debug': {
        'level': 'WARNING',
        'filters': ['require_debug_false'],
        'class': 'logging.StreamHandler',
    },
    'django.server': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'django.server',
    },
    '''
    'mail_admins': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'django.utils.log.AdminEmailHandler'
    },
    '''
    'gunicorn': {
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'django.server',
        'filename': '/home/www-data/dj/opentrafficweb/opentrafficweb/log/gunicorn/error.log',
        'maxBytes': 1024 * 1024 * 32,  # 32 mb
    }
},
'loggers': {
    'django': {
        'handlers': ['console', 'console_on_not_debug', 'gunicorn'],  # 'mail_admins'
        'level': 'INFO',
    },
    'django.server': {
        'handlers': ['django.server'],
        'level': 'INFO',
        'propagate': False,
    },
}
}

'''
# https://stackoverflow.com/questions/21943962/how-to-see-details-of-django-errors-with-gunicorn
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/home/www-data/dj/opentrafficweb/opentrafficweb/log/gunicorn/error.log',
            'maxBytes': 1024 * 1024 * 32,  # 32 mb
        }
    },
    'loggers': {
        'gunicorn.errors': {
            'level': 'DEBUG',
            'handlers': ['gunicorn'],
            'propagate': True,
        },
    }
}
'''
