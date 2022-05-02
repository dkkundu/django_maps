"""API > serializers > user.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
# DRF IMPORTS
from rest_framework import serializers
# API IMPORTS
from API.serializers import ProfileSerializer


logger = logging.getLogger(__name__)
USER_MODEL = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User and Profile models"""
    profile = ProfileSerializer(required=False)

    class Meta:
        """Meta class"""
        model = USER_MODEL
        fields = '__all__'
        read_only_fields = (
            'last_login', 'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,  # does not expose field in GET
                'min_length': 8,  # minimum length of password
                'style': {'input_type': 'password'},  # for browsable API
            },
        }

    def create(self, validated_data):
        """Overriding to handle with custom user manager"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating user: email={validated_data.get('email', None)}"
        )
        profile_data = validated_data.pop('profile', None)
        user = USER_MODEL.objects.create_user(**validated_data)
        if profile_data:  # takes profile dict, sets attrs, saves profile obj
            self.update_profile(user.profile, profile_data)
        return user

    def update(self, instance, validated_data):
        """Overriding to handle setting password correctly"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Updating user: email={validated_data.get('email', None)}"
        )
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if profile_data:  # takes profile dict, sets attrs, saves profile obj
            self.update_profile(user.profile, profile_data)
        if password:  # takes raw password, hashes password then sets password
            self.update_password(user, password)
        return user

    def update_profile(self, instance, validated_data):
        """Updates the profile of the user with validated data"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Updating profile: email={instance.user.email}"
        )
        for k, v in validated_data.items():
            # if value is empty, set to None for unique fields else Integrity
            if v == '' and instance._meta.get_field(k).unique:
                v = None  # fixes duplication error with unique fields and ""
            setattr(instance, k, v)
        instance.save()

    def update_password(self, user, password):
        """Updates the user password properly"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Updating password: email={user.email}"
        )
        user.set_password(password)
        user.save()
