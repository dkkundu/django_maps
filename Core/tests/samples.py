"""Core > tests > samples.py"""
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


USER_MODEL = get_user_model()


def sample_user(email="user@sample.com", password="samplepwd", **kwargs):
    """Sample user to be used for tests"""
    return USER_MODEL.objects.create_user(email, password, **kwargs)


def sample_staffuser(email="staff@email.com", password="staffpass", **kwargs):
    """Sample staffuser to be used for tests"""
    return USER_MODEL.objects.create_staffuser(email, password, **kwargs)


def sample_superuser(email="super@email.com", password="superpass", **kwargs):
    """Sample superuser to be used for tests"""
    return USER_MODEL.objects.create_superuser(email, password, **kwargs)


def get_perm(action, model):
    """Returns permission object with given action and model"""
    return Permission.objects.get(name=f"Can {action.lower()} {model.lower()}")
