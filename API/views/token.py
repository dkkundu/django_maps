"""API > views > token.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DRF IMPORTS
from django.utils import timezone
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
# API IMPORTS
from API.serializers import TokenSerializer, LogoutSerializer, UserSerializer

logger = logging.getLogger(__name__)


class ObtainTokenView(ObtainAuthToken):
    """Gets a authentication token for user with provided credentials"""
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Obtaining token: email={request.POST.get('email')}"
        )
        # return super().post(request, *args, **kwargs)
        # Overridden to return more user information with token

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serialized_user = UserSerializer(user)

        user.last_login = timezone.now()
        user.save()  # save the last login time to now()

        data = {'token': token.key}
        data.update(serialized_user.data)
        return Response(data)


class LogoutView(generics.DestroyAPIView):
    """Delete token upon user logout"""
    serializer_class = LogoutSerializer
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
    )  # auth class not required because set as default in settings
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Overriding for complex check and returns token"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Retrieving token: email={self.request.POST.get('email')}"
        )
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        obj = get_object_or_404(
            Token, user=user, key=serializer.validated_data['token']
        )

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
