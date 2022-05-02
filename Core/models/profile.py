"""Core > models > profile.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DJANGO IMPORTS
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# CORE IMPORTS
from Core.models import User
# PROMETHEUS IMPORTS
from django_prometheus.models import ExportModelOperationsMixin


logger = logging.getLogger(__name__)


def media_upload_path(instance, filename):
    """Returns formatted upload to path"""
    path = f'Users/{instance.user.id}/{filename}'
    logger.debug(  # prints class and function name
        f"{_getframe().f_code.co_name} Media upload path: {path}"
    )
    return path


class Profile(ExportModelOperationsMixin('profile'), models.Model):
    """User Profile model"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, unique=True
    )
    image = models.ImageField(
        _('Profile Picture'), blank=True, null=True,
        upload_to=media_upload_path
    )
    bio = models.TextField(
        _('Bio'), blank=True, null=True
    )
    website = models.URLField(
        _('Website'), blank=True, null=True
    )
    birthday = models.DateField(
        _('Date of Birth'), blank=True, null=True
    )
    gender = models.CharField(
        _('Gender'), max_length=1, blank=True, null=True,
        choices=[('M', 'Male'), ('F', 'Female')]
    )
    spouse_name = models.CharField(
        _('Name of Spouse'), max_length=255, blank=True, null=True
    )
    father_name = models.CharField(
        _('Name of Father'), max_length=255, blank=True, null=True
    )
    mother_name = models.CharField(
        _('Name of Mother'), max_length=255, blank=True, null=True
    )
    nid = models.CharField(
        _('National ID'), max_length=17, unique=True, blank=True, null=True,
        validators=[RegexValidator(
            r'^(\d{10}|\d{13}|\d{17})$',
            message='Numeric 10/13/17 digits (ex: 1234567890)'
        )]
    )
    passport = models.CharField(
        _('Passport'), max_length=9, unique=True, blank=True, null=True,
        validators=[RegexValidator(
            r'^[A-Z]{2}\d{7}$',
            message='Alphanumeric 9 characters (ex: PA3456789)'
        )]
    )
    address = models.CharField(
        _('Street Address'), max_length=255, blank=True, null=True
    )
    thana = models.CharField(
        _('Thana'), max_length=255, blank=True, null=True
    )
    district = models.CharField(
        _('District'), max_length=255, blank=True, null=True
    )
    division = models.CharField(
        _('Division'), max_length=255, blank=True, null=True
    )
    postal = models.CharField(
        _('Postal Code'), max_length=4, blank=True, null=True
    )
    is_active = models.BooleanField(
        _('Active'), default=True, null=True
    )
    created_at = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )

    @property
    def age(self):
        """Returns user's age from given birthday, else returns 0"""
        age = 0
        if self.birthday:
            age = int((timezone.now().date() - self.birthday).days / 365.25)
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Calculated {self.user}'s age: {age}"
        )
        return age

    def __str__(self):
        """String representation of Profile model"""
        return self.user.email


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Creates or updates profile, when User object changes"""
    if created:
        logger.debug(  # prints class and function name
            f"{_getframe().f_code.co_name} Creating {instance}'s profile"
        )
        Profile.objects.get_or_create(user=instance)
    logger.debug(  # prints class and function name
        f"{_getframe().f_code.co_name} Saving {instance}'s profile"
    )
    instance.profile.save()
