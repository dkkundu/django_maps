"""Core > forms > user.py"""
# DJANGO IMPORTS
from django import forms
from django.contrib.auth import get_user_model
# CORE IMPORTS
from Core.models import Profile


USER_MODEL = get_user_model()


class UserUpdateForm(forms.ModelForm):
    """User model form for create and update"""

    class Meta:
        """Meta class"""
        model = USER_MODEL
        fields = ('first_name', 'last_name', 'email', 'phone')


class ProfileUpdateForm(forms.ModelForm):
    """Profile model update form"""

    class Meta:
        """Meta class"""
        model = Profile
        exclude = ('user', 'is_active', 'created_at', 'last_updated')
