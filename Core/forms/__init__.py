"""Core > forms > __init__.py"""
from .registration import SignupForm
from .user import UserUpdateForm, ProfileUpdateForm

# update the following list to allow classes to be available for import
# this is very useful especially when using from .file import *
__all__ = [SignupForm, UserUpdateForm, ProfileUpdateForm, ]
