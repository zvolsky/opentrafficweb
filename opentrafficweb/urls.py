"""opentrafficweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('allauth.urls')),
    path('pokus/', include('pokus.urls')),
    path('jsi18n/',
         last_modified(lambda req, **kw: last_modified_date)(
             cache_page(86400, key_prefix='jsi18n')(JavaScriptCatalog.as_view(packages=['fex']))
         ), name='jsi18n'),

    # shopon non-i18n urls (all, that is not needed for search engines)
    # path('', include('urls_not_i18n')),
]

'''
urlpatterns.extend(
    i18n_patterns(
        path('', include('urls_i18n'))
    )
)
'''

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
