"""Core > tests > views > test_admin.py"""
# PYTHON IMPORTS
from http import HTTPStatus
# DJANGO IMPORTS
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
# CORE IMPORTS
from Core.tests.samples import sample_user, sample_staffuser, sample_superuser


USER_MODEL = get_user_model()
ADMIN_URL = f"/{settings.ADMIN_URL}"
LOGIN_URL = f"{ADMIN_URL}/login"


class AdminPublicTests(TestCase):
    """Tests Admin View for anonymous users"""
    def setUp(self):
        """setup"""
        self.client = Client()

    def test_public_view(self):
        """Tests that anonymous user is redirected to login"""
        response = self.client.get(ADMIN_URL, follow=True)
        self.assertRedirects(
            response, f"{LOGIN_URL}/?next={ADMIN_URL}/",
            status_code=HTTPStatus.MOVED_PERMANENTLY,
            target_status_code=HTTPStatus.OK
        )


class UserListPrivateTests(TestCase):
    """Tests Admin View for authenticated users"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.staffuser = sample_staffuser()
        self.superuser = sample_superuser()
        self.client = Client()
        self.client.login(email="user@sample.com", password="samplepwd")

    def test_user_view(self):
        """Tests Admin View for normal user"""
        response = self.client.get(ADMIN_URL, follow=True)
        self.assertRedirects(
            response, f"{LOGIN_URL}/?next={ADMIN_URL}/",
            status_code=HTTPStatus.MOVED_PERMANENTLY,
            target_status_code=HTTPStatus.OK
        )

    def test_staff_user_view(self):
        """Tests Admin View for staffuser"""
        self.client.login(email="staff@email.com", password="staffpass")

        response = self.client.get(ADMIN_URL, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK

    def test_super_user_view(self):
        """Tests Admin View for superuser"""
        self.client.login(email="super@email.com", password="superpass")

        response = self.client.get(ADMIN_URL, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
