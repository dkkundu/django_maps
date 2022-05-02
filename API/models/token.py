"""API > models > token.py"""
# PYTHON IMPORTS
import logging
# DJANGO IMPORTS
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# DRF IMPORTS
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


# Setting up a Token model receiver on post_save of User model so a token is
# generated automatically on creation of a new user. The signal has to be on a
# model file so that it is loaded on Django start up during model scans
# https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create an authentication token for the new user"""
    if created:
        Token.objects.get_or_create(user=instance)
