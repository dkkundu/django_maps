"""DJMAPS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# DJANGO IMPORTS
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
# CORE IMPORTS
from Core.views import IndexView, SignupView, LoginView

urlpatterns = [
    # index url ---------------------------------------------------------------
    path('', IndexView.as_view(), name='index'),

    # prometheus url ----------------------------------------------------------
    path('', include('django_prometheus.urls')),

    # admin urls --------------------------------------------------------------
    path(f'{settings.ADMIN_URL}/', admin.site.urls),

    # Core urls ---------------------------------------------------------------
    path('core/', include('Core.urls')),

    # API urls ----------------------------------------------------------------
    path('api/', include('API.urls')),

    # auth urls ---------------------------------------------------------------
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/', include('django.contrib.auth.urls')),

    # drf api auth ------------------------------------------------------------
    path('api-auth/', include('rest_framework.urls')),
]

# serve media files in development environment --------------------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# debug toolbar ---------------------------------------------------------------
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# admin site customizations ---------------------------------------------------
admin.sites.AdminSite.site_header = "DJMAPS Administration"
admin.sites.AdminSite.site_title = "DJMAPS Administration"
admin.sites.AdminSite.index_title = "DJMAPS Admin Panel"
