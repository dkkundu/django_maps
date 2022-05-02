"""API > serializers > token.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DJANGO IMPORTS
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.base_user import BaseUserManager
# DRF IMPORTS
from rest_framework import serializers

logger = logging.getLogger(__name__)


class TokenSerializer(serializers.Serializer):
    """Authentication Token Serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False  # password may contain spaces
    )

    def validate(self, attrs):
        """token validation and authentication"""
        email = BaseUserManager.normalize_email(attrs.get('email'))
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Validating user: email={email}"
        )
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=attrs.get('password')
        )
        if not user:
            logger.debug(  # prints class and function name
                f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
                f"Authentication failed: email={email}"
            )
            raise serializers.ValidationError(
                "Unable to authenticate user with provided credentials",
                code='authentication'
            )
        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    """Returns user object from matching user id and email"""
    token = serializers.CharField()
    email = serializers.EmailField()
    id = serializers.IntegerField()

    def validate(self, attrs):
        """validates provided user id and email"""
        email = BaseUserManager.normalize_email(attrs.get('email'))
        user_id = attrs.get('id')
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Retrieving user: email={email}, id={user_id}"
        )
        try:
            user = get_user_model().objects.get(id=user_id, email=email)
        except Exception:
            user = None
            logger.debug(  # prints class and function name
                f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
                f"Validation failed: email={email}, id={user_id}"
            )
            raise serializers.ValidationError(
                "Unable to retrieve user with provided data",
                code='validation'
            )
        attrs['user'] = user
        return attrs
