"""API > tests > views > token.py"""
# DJANGO IMPORTS
from django.test import TestCase
from django.urls import reverse
# DRF IMPORTS
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
# CORE IMPORTS
from Core.tests import samples, utils

LOGIN_URL = reverse('api:auth-login')
LOGOUT_URL = reverse('api:auth-logout')


class PublicTokenAPITests(TestCase):
    """Tests API for token requests on token endpoints"""
    def setUp(self):
        """setup the client"""
        self.client = APIClient()

    def test_token_obtain(self):
        """Tests a user can obtain an authentication token"""
        data = {'email': 'test@email.com', 'password': 'te$tpwd1'}
        samples.sample_user(**data)
        response = self.client.post(LOGIN_URL, data)
        # asserts
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('email', response.data)
        self.assertIn('id', response.data)

    @utils.suppress_warnings
    def test_token_invalid_credentials(self):
        """Tests token API response for invalid credentials"""
        samples.sample_user('test@email.com', 'te$tpwd1')
        data = {'email': 'test@email.com', 'password': 'invalid1'}
        response = self.client.post(LOGIN_URL, data)
        # asserts
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    @utils.suppress_warnings
    def test_token_no_user(self):
        """Tests token API for no user or email in database"""
        data = {'email': 'test@email.com', 'password': 'te$tpwd1'}
        response = self.client.post(LOGIN_URL, data)
        # asserts
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    @utils.suppress_warnings
    def test_token_missing_data(self):
        """Tests token API with missing data"""
        samples.sample_user('test@email.com', 'te$tpwd1')
        data = {'email': 'test@email.com', 'password': ''}
        response = self.client.post(LOGIN_URL, data)
        # asserts
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


class PrivateTokenAPITests(TestCase):
    """Test API on private endpoints using token"""
    def setUp(self):
        """setup api client and sample users and tokens"""
        self.data = {"email": "delete@token.com", "password": "d3l3t3T0k3n"}
        self.user = samples.sample_user(**self.data)

        self.client = APIClient()
        response = self.client.post(LOGIN_URL, self.data)
        self.token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_token_delete_on_logout(self):
        """Tests the deletion of token on user logout"""
        response = self.client.delete(LOGOUT_URL, data={
            'id': self.user.id,
            'email': self.user.email,
            'token': self.token
        })
        token_exists = Token.objects.filter(key=self.token).exists()
        self.assertFalse(token_exists)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
