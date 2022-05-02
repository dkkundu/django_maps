"""API > views > profile.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DRF IMPORTS
from rest_framework import generics
# CORE IMPORTS
from Core.models import Profile
# API IMPORTS
from API.serializers import ImageSerializer


logger = logging.getLogger(__name__)


class ImageUploadAPI(generics.RetrieveUpdateAPIView):
    """Retrieves and/or Updates the Image field in the Profile Model"""
    queryset = Profile.objects.all()
    serializer_class = ImageSerializer
    # authentication_classes = ()  # check defaults in settings
    # permission_classes = ()  # check defaults in settings

    def retrieve(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Retrieving profile: "
            f"{self.lookup_field}={kwargs[self.lookup_field]}"
        )
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Updating profile: "
            f"{self.lookup_field}={kwargs[self.lookup_field]}"
        )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Partial update profile: "
            f"{self.lookup_field}={kwargs[self.lookup_field]}"
        )
        return super().partial_update(request, *args, **kwargs)
