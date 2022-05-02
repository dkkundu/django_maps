"""Core > tests > views > test_registration.py"""
# PYTHON IMPORTS
from http import HTTPStatus
import logging
# DJANGO IMPORTS
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
# CORE IMPORTS
from Core.tests.samples import sample_user
from Core.tests.utils import suppress_warnings, suppress_errors


USER_MODEL = get_user_model()
LOGIN_URL = settings.LOGIN_URL
SIGNUP_URL = '/auth/signup/'


class SignupPublicTests(TestCase):
    """Tests Signup View for anonymous users"""
    def setUp(self):
        """setup"""
        self.client = Client()

    def test_get_method(self):
        """Tests the view with anonymous user"""
        response = self.client.get(SIGNUP_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_valid_post_method(self):
        """Tests valid signup for user"""
        response = self.client.post(SIGNUP_URL, {
            'email': 'testuser@email.com',
            'password1': 'qw3rtyu1',
            'password2': 'qw3rtyu1',
        }, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertTrue(
            USER_MODEL.objects.filter(email='testuser@email.com').exists()
        )

    @suppress_errors
    def test_invalid_email_post_method(self):
        """Tests invalid signup for user"""
        logging.disable(logging.CRITICAL)  # only critical level log output
        response = self.client.post(SIGNUP_URL, {
            'email': 'testuser',
            'password1': 'qw3rtyu1',
            'password2': 'qw3rtyu1',
        }, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # back to same
        self.assertFalse(
            USER_MODEL.objects.filter(email='testuser@email.com').exists()
        )
        logging.disable(logging.NOTSET)  # reset logging level

    @suppress_errors
    def test_invalid_password_post_method(self):
        """Tests invalid signup for user"""
        logging.disable(logging.CRITICAL)  # only critical level log output
        response = self.client.post(SIGNUP_URL, {
            'email': 'testuser@email.com',
            'password1': 'qwertyu1',
            'password2': 'qw3rtyui',
        }, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # back to same
        self.assertFalse(
            USER_MODEL.objects.filter(email='testuser@email.com').exists()
        )
        logging.disable(logging.NOTSET)  # reset logging level

    @suppress_warnings
    def test_other_methods(self):
        """Tests all methods other than get/post"""
        # response = self.client.put(SIGNUP_URL)  # 200 OK
        # self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.patch(SIGNUP_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.delete(SIGNUP_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.trace(SIGNUP_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


class SignupPrivateTests(TestCase):
    """Tests Signup View for authenticated users"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.client = Client()
        self.client.login(email='user@sample.com', password='samplepwd')

    def test_private_view(self):
        """Tests signup view for authenticated users"""
        response = self.client.get(SIGNUP_URL)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # redirected
        self.assertEqual(response.url, '/')  # redirected to index
        self.assertFalse(response.wsgi_request.user.is_anonymous)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    @suppress_warnings
    def test_other_methods(self):
        """Tests all methods other than get/post"""
        response = self.client.post(SIGNUP_URL)  # 302 redirect
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/')
        response = self.client.put(SIGNUP_URL)  # 302 mirrors post method
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/')
        response = self.client.patch(SIGNUP_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.delete(SIGNUP_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.trace(SIGNUP_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


class LoginPublicTests(TestCase):
    """Tests user login and authentication for anonymous users"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.client = Client()

    def test_get_method(self):
        """Tests the view with anonymous user"""
        response = self.client.get(LOGIN_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_valid_post_method(self):
        """Tests valid login for user"""
        response = self.client.post(LOGIN_URL, {
            'username': 'user@sample.com', 'password': 'samplepwd'
        }, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertFalse(response.wsgi_request.user.is_anonymous)

    @suppress_errors
    def test_invalid_email_post_method(self):
        """Tests invalid login for user using wrong email"""
        response = self.client.post(LOGIN_URL, {
            'username': 'user@sample.net', 'password': 'samplepwd',
        }, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # back to same
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_anonymous)

    @suppress_errors
    def test_invalid_password_post_method(self):
        """Tests invalid login for user using wrong password"""
        response = self.client.post(LOGIN_URL, {
            'username': 'user@sample.com', 'password': 'samplepasswd',
        }, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # back to same
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_anonymous)

    @suppress_warnings
    def test_other_methods(self):
        """Tests all methods other than get/post"""
        response = self.client.put(LOGIN_URL)  # 200 OK
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.patch(LOGIN_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.delete(LOGIN_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.trace(LOGIN_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


class LoginPrivateTests(TestCase):
    """Tests user login for authenticated users"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.client = Client()
        self.client.login(email='user@sample.com', password='samplepwd')

    def test_private_view(self):
        """Tests login view for authenticated users"""
        response = self.client.get(LOGIN_URL)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # redirected
        self.assertEqual(response.url, '/')  # redirected to index
        self.assertFalse(response.wsgi_request.user.is_anonymous)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    @suppress_warnings
    def test_other_methods(self):
        """Tests all methods other than get/post"""
        response = self.client.post(LOGIN_URL)  # 302 redirect
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/')
        response = self.client.put(LOGIN_URL)  # 302 mirrors post method
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/')
        response = self.client.patch(LOGIN_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.delete(LOGIN_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.trace(LOGIN_URL)  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
