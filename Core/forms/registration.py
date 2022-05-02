"""Core > forms > registration.py"""
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


USER_MODEL = get_user_model()


class SignupForm(UserCreationForm):
    """New user registration and signup form"""

    class Meta:
        """Meta class"""
        model = USER_MODEL
        fields = ('first_name', 'last_name', 'email', 'phone')
