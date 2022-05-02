"""Core > views > index.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DJANGO IMPORTS
from django.contrib import messages
from django.contrib.auth import get_user_model, views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import ugettext_lazy as _
# CORE IMPORTS
from Core.forms import SignupForm


logger = logging.getLogger(__name__)
USER_MODEL = get_user_model()


# - LoginView, LogoutView used from django.contrib.auth.views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks clicked link and prompts for a new password
# - PasswordResetCompleteView shows a success message for the above


def redirect_auth_users(request, message=None):
    """Redirect authenticated users to index view"""
    logger.debug(  # prints function name and description
        f"{_getframe().f_code.co_name} "
        f"Redirecting {request.user} to IndexView..."
    )
    if not message:  # default message
        message = _(f"{request.user}, you are redirected to Index page.")
    messages.info(request=request, message=message)
    return redirect(reverse_lazy('index'))


class SignupView(CreateView):
    """New user registration and signup view"""
    model = USER_MODEL
    form_class = SignupForm
    template_name = 'registration/signup.html'

    @staticmethod
    def get_redirect_message(request):
        """Returns a message to user when redirected"""
        return _(
            f"You are already registered as {request.user}. "
            f"Redirected you to Index page. "
            f"Please logout if you wish to create a new user."
        )

    def get(self, request, *args, **kwargs):
        """GET method"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"{request.user} is authenticated: {request.user.is_authenticated}"
        )
        # redirect authenticated users
        if request.user.is_authenticated:
            return redirect_auth_users(
                request=request, message=self.get_redirect_message(request)
            )

        # if user is not authenticated, proceed with SignupView
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """POST method"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Performing form validation..."
        )
        # redirect authenticated users
        if request.user.is_authenticated:
            return redirect_auth_users(
                request=request, message=self.get_redirect_message(request)
            )

        # if user is not authenticated, proceed with SignupView
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """form is clean and validated"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Form is clean and valid. Saving {form}"
        )
        self.object = form.save()
        self.object.refresh_from_db()  # creates profile instance via signals

        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"User account was created for {self.object}."
        )
        message = _(
            f"{self.object}, your user account was created successfully. "
            f"Please login using your email address and password."
        )
        messages.success(request=self.request, message=message)
        return redirect(reverse_lazy('login'))

    def form_invalid(self, form):
        """form is invalid"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Form is invalid. {form}"
        )
        logger.error(form.errors)  # log all form errors
        message = _("Validation error, please check all fields for any error.")
        messages.error(request=self.request, message=message)
        return super().form_invalid(form)


class LoginView(views.LoginView):
    """Overriding Django LoginView from django.contrib.auth.views"""

    @staticmethod
    def get_redirect_message(request):
        """Returns a message to user when redirected"""
        return _(
            f"You are already logged in as {request.user}. "
            f"Redirected you to Index page. "
            f"Please logout if you wish to log in as a new user."
        )

    def get(self, request, *args, **kwargs):
        """overriding GET method"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"{request.user} is authenticated: {request.user.is_authenticated}"
        )
        # redirect authenticated users
        if request.user.is_authenticated:
            return redirect_auth_users(
                request=request, message=self.get_redirect_message(request)
            )

        # if user is not authenticated, proceed with LoginView
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """overriding POST method"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Performing form validation..."
        )
        # redirect authenticated users
        if request.user.is_authenticated:
            return redirect_auth_users(
                request=request, message=self.get_redirect_message(request)
            )

        # if user is not authenticated, proceed with LoginView
        return super().post(request, *args, **kwargs)
