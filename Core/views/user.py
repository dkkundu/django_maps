"""Core > views > user.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# CORE IMPORTS
from Core.forms import SignupForm, UserUpdateForm, ProfileUpdateForm
from Core.models import Profile
# PROJECT IMPORTS
from utils import test_user


logger = logging.getLogger(__name__)
USER_MODEL = get_user_model()


class UserListView(
    UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin,
    ListView
):
    """List view for User model"""
    model = USER_MODEL
    paginate_by = 100  # default
    ordering = ('id', )  # default; needed to avoid pagination inconsistency
    permission_required = 'Core.view_user'
    template_name = 'Core/user/list.html'

    def test_func(self):
        """Tests if user is_active and is_staff/is_superuser"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Testing {self.request.user} status"
        )
        return test_user(self.request.user)


class UserDetailView(
    UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin,
    DetailView
):
    """Detail view for User model"""
    model = USER_MODEL
    permission_required = ('Core.view_user', 'Core.view_profile')
    template_name = 'Core/user/detail.html'

    def test_func(self):
        """Tests if user is_active and is_staff/is_superuser"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Testing {self.request.user} status"
        )
        obj = self.get_object()

        # tests if the user is the same as the object he is trying to view
        is_owner = (obj == self.request.user) and self.request.user.is_active

        return is_owner or test_user(self.request.user)


class UserCreateView(
    UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin,
    CreateView
):
    """Create view for user model"""
    model = USER_MODEL
    form_class = SignupForm
    permission_required = 'Core.add_user'
    template_name = 'Core/user/create.html'

    def test_func(self):
        """Tests if user is_active and is_staff/is_superuser"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Testing {self.request.user} status"
        )
        return test_user(self.request.user)

    def get_success_url(self):
        """Overriding to redirect to detail view"""
        url = reverse_lazy('core:user_detail', kwargs={'pk': self.object.pk})
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Generated success url: {url}"
        )
        return url


class UserUpdateView(
    UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin,
    UpdateView
):
    """Update view for user model. Can also be used as detail view"""
    model = USER_MODEL
    form_class = UserUpdateForm
    form2_class = ProfileUpdateForm
    permission_required = ('Core.change_user', 'Core.change_profile')
    template_name = 'Core/user/update.html'

    def test_func(self):
        """Tests if user is_active and is_staff/is_superuser"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Testing {self.request.user} status"
        )
        obj = self.get_object()

        # tests if the user is the same as the object he is trying to update
        is_owner = (obj == self.request.user) and self.request.user.is_active

        # tests if user instance is_staff/is_superuser, then staff not allowed
        staff_allowed = True
        if obj.is_staff or obj.is_superuser:
            staff_allowed = False

        # tests for is_superuser and is_active
        is_superuser = self.request.user.is_superuser and \
            self.request.user.is_active

        return is_owner or staff_allowed or is_superuser

    def get_form2_kwargs(self):
        """Copies get_form_kwargs() to include profile form kwargs"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Getting profile form keyword arguments..."
        )

        kwargs = self.get_form_kwargs()
        kwargs.update({
            'instance': Profile.objects.get(user=self.get_object())
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Overriding to include profile form and extra data"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Getting context data..."
        )

        if 'form2' not in kwargs:
            kwargs['form2'] = self.form2_class(**self.get_form2_kwargs())
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """Overriding post method to include profile form validation"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"POST form data for user: {request.user}"
        )

        self.object = self.get_object()
        form = self.get_form()  # user form
        form2 = self.form2_class(**self.get_form2_kwargs())  # profile form

        if form.is_valid() and form2.is_valid():
            form2.save()  # saves profile object
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """Overriding to redirect to detail view"""
        url = reverse_lazy('core:user_detail', kwargs={'pk': self.object.pk})
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Generated success url: {url}"
        )
        return url
