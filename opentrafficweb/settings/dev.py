from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e^+j630&uymk*6ku_u4+*e744ftl993v5$adwgwk!x1+*5l^!6'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'   # run ./MailHog
EMAIL_PORT = 1025          # navigate to localhost:8025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False


try:
    from .local import *
except ImportError:
    pass

DEBUG_TOOLBAR = bool(os.getenv('DDT', False))
if DEBUG_TOOLBAR:
    INTERNAL_IPS = ['127.0.0.1']
    MIDDLEWARE.append(
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_CONFIG = {
        # 'SHOW_TOOLBAR_CALLBACK': False,
        'INTERCEPT_REDIRECTS': False,
    }
