"""API > views > __init__.py"""
from .profile import ImageUploadAPI
from .user import UserCreateView, UserViewSet
from .token import ObtainTokenView, LogoutView

# update the following list to allow classes to be available for import
# this is very useful especially when using from .file import *
__all__ = [
    ImageUploadAPI, UserCreateView, UserViewSet, ObtainTokenView, LogoutView
]
