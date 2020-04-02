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
            'filename': '/home/www-data/dj/opentrafficweb/opentrafficweb/log/nginx/gunicorn-error.log',
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
