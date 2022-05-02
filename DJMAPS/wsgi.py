"""
WSGI config for DJMAPS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
# PYTHON IMPORTS
import os
# DJANGO IMPORTS
from django.core.wsgi import get_wsgi_application


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DJMAPS.settings'
)

application = get_wsgi_application()
