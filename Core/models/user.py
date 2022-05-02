"""Core > models > test_user.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DJANGO IMPORTS
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
# PROMETHEUS IMPORTS
from django_prometheus.models import ExportModelOperationsMixin


logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    """User Manager overridden from BaseUserManager for User"""

    def _create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        if not email:  # check for an empty email
            logger.error(  # prints class and function name
                f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
                f"User must set an email address"
            )
            raise AttributeError("User must set an email address")
        else:  # normalizes the provided email
            email = self.normalize_email(email)
            logger.debug(  # prints class and function name
                f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
                f"Normalized email: {email}"
            )

        # create user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # safe for multiple databases
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"User created: {user}"
        )
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating user: email={email}, extra_fields={extra_fields}"
        )
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None, **extra_fields):
        """Creates and returns a new staffuser using an email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating staffuser: email={email}, extra_fields={extra_fields}"
        )
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a new superuser using an email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating superuser: email={email}, extra_fields={extra_fields}"
        )
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin,
           ExportModelOperationsMixin('user')):
    """User model that supports using email instead of username"""
    email = models.EmailField(
        _('Email Address'), max_length=255, unique=True, blank=False, null=True
    )
    phone = models.CharField(
        _('Mobile Phone'), max_length=12, blank=True, null=True,
        validators=[RegexValidator(  # min: 10, max: 12 characters
            r'^[\d]{10,12}$', message='Format (ex: 0123456789)'
        )]
    )
    first_name = models.CharField(
        _('First Name'), max_length=255, blank=True, null=True
    )
    last_name = models.CharField(
        _('Family Name'), max_length=255, blank=True, null=True
    )
    is_staff = models.BooleanField(
        _('Staff status'), default=False, null=True
    )
    is_active = models.BooleanField(
        _('Active'), default=True, null=True
    )
    date_joined = models.DateTimeField(
        _('Date Joined'), auto_now_add=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )

    objects = UserManager()  # uses the custom manager

    USERNAME_FIELD = 'email'  # overrides username to email field

    def get_full_name(self):
        """Returns full name of User
        Return None if no names are set"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Getting {self.email}'s full name"
        )
        full_name = None  # default

        # join first name and last name
        if self.first_name:
            full_name = ''.join(self.first_name)
            if self.last_name:
                full_name += f' {self.last_name}'
        else:
            if self.last_name:
                full_name = ''.join(self.last_name)

        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Returning user's full name: {full_name}"
        )
        return full_name  # returns None if no name is set

    def get_phone_intl_format(self, prefix='+88'):
        """Returns phone number in international format
        Default prefix: +88 (Bangladesh code)
        Returns None if user has no phone number saved"""
        phone_intl = f'{prefix}{self.phone}' if self.phone else None
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Returning phone number in international format: {phone_intl}"
        )
        return phone_intl

    def __str__(self):
        """User model string representation"""
        return self.email
