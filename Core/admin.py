"""Core > admin.py"""
# PYTHON IMPORTS
import logging
# DJANGO IMPORTS
from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
# PLUGIN IMPORTS
from import_export import resources
from import_export.admin import (
    ImportExportModelAdmin, ImportExportActionModelAdmin)
# PROJECT IMPORTS
from Core import models

logger = logging.getLogger(__name__)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Django Admin Log Entries"""
    date_hierarchy = 'action_time'
    list_display = ('action_time', 'user_link', 'content_type', 'object_link',
                    'action_flag', 'change_message')
    list_filter = ('action_flag', 'content_type')
    search_fields = ('user__first_name', 'user__last_name', 'user__email',
                     'user__phone', 'object_repr', 'change_message')

    def has_add_permission(self, request):
        """Permission to ADD a LogEntry"""
        return False

    def has_change_permission(self, request, obj=None):
        """Permission to CHANGE a LogEntry"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Permission to DELETE a LogEntry"""
        return False

    def has_view_permission(self, request, obj=None):
        """Permission to VIEW a LogEntry"""
        return request.user.is_superuser

    def user_link(self, obj):
        """Show link to the User"""
        try:
            url = reverse('admin:core_user_change', args=[obj.user_id])
            link = f'<a href="{url}">{escape(obj.user)}</a>'
        except Exception as e:
            logger.debug(e)
            link = escape(obj.user)
        return mark_safe(link)

    user_link.admin_order_field = "user"
    user_link.short_description = "user"

    def object_link(self, obj):
        """Show link to the object"""
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            try:
                ct = obj.content_type
                url = reverse(f'admin:{ct.app_label}_{ct.model}_change',
                              args=[obj.object_id])
                link = f'<a href="{url}">{escape(obj.object_repr)}</a>'
            except Exception as e:
                logger.debug(e)
                link = escape(obj.object_repr)
        return mark_safe(link)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


class ProfileInline(admin.StackedInline):
    """Stacked inline profile view under User model"""
    model = models.Profile
    can_delete = False
    max_num = 1
    verbose_name = 'Profile'
    verbose_name_plural = 'Profile'


class UserResource(resources.ModelResource):
    """
    User model import_export resource
    https://django-import-export.readthedocs.io/en/stable/index.html
    """
    class Meta:
        """Meta class"""
        model = models.User


@admin.register(models.User)
class UserAdmin(
    ImportExportActionModelAdmin, ImportExportModelAdmin, UserAdmin
):
    """Admin for User model"""
    ordering = ('email', )
    list_display = (
        'email', 'first_name', 'last_name', 'phone', 'last_login',
        'last_updated', 'date_joined', 'is_staff', 'is_superuser', 'is_active',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Roles', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Dates', {'fields': ('last_login', 'last_updated', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                'email', 'first_name', 'last_name', 'phone',
                'password1', 'password2'
            )
        }),
    )
    readonly_fields = ('last_login', 'last_updated', 'date_joined')
    search_fields = ('id', 'email', 'first_name', 'last_name', 'phone')
    inlines = (ProfileInline, )
    resource_class = UserResource  # import_export

    def get_inline_instances(self, request, obj=None):
        """hides inlines during 'add user' view"""
        return obj and super().get_inline_instances(request, obj) or []
