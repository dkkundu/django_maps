"""Core > tests > views > test_index.py"""
# PYTHON IMPORTS
from http import HTTPStatus
# DJANGO IMPORTS
from django.test import Client, TestCase
# CORE IMPORTS
from Core.tests.samples import sample_user
from Core.tests.utils import suppress_warnings


class IndexPublicTests(TestCase):
    """Tests the landing page for anonymous users"""

    def setUp(self):
        """setup"""
        self.client = Client()

    def test_index_template(self):
        """Tests index view template use"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertTemplateUsed(response, 'index.html')

    def test_public_view(self):
        """Tests index view for anonymous users"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    @suppress_warnings
    def test_other_methods(self):
        """tests all methods other than get"""
        response = self.client.post('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.put('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.patch('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.delete('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.trace('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


class IndexPrivateTest(TestCase):
    """Tests the landing page for authenticated users"""

    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.client = Client()
        self.client.login(email='user@sample.com', password='samplepwd')

    def test_index_template(self):
        """Tests index view template use"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertTemplateUsed(response, 'index.html')

    def test_private_view(self):
        """Tests index view for authenticated users"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertFalse(response.wsgi_request.user.is_anonymous)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    @suppress_warnings
    def test_other_methods(self):
        """Tests all methods other than get"""
        response = self.client.post('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.put('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.patch('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.delete('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = self.client.trace('/')  # 405 method not allowed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
