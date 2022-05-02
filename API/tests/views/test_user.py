"""API > tests > views > user.py"""
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
# DRF IMPORTS
from rest_framework import status
from rest_framework.test import APIClient
# CORE IMPORTS
from Core.tests import samples, utils

LOGIN_URL = reverse('api:auth-login')
SIGNUP_URL = reverse('api:auth-signup')
USERS_URL = reverse('api:user-list')


def get_detail_url(pk):
    """Return user detail url"""
    return reverse('api:user-detail', args=[pk])


class PublicUserAPITests(TestCase):
    """Tests API for non-authenticated requests on Users endpoints"""
    def setUp(self):
        """setup the client"""
        self.client = APIClient()

    def test_user_create(self):
        """Tests API for creating a new user"""
        data = {'email': 'test@email.com', 'password': 'te$tpwd1'}
        response = self.client.post(SIGNUP_URL, data)
        user = get_user_model().objects.get(id=response.data.get('id'))
        # asserts
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, data.get('email'))
        self.assertTrue(user.check_password(data.get('password')))
        self.assertNotIn('password', response.data)

    @utils.suppress_warnings
    def test_user_create_duplicate(self):
        """Tests API for new user with same email (duplicates)"""
        data = {'email': 'test@email.com', 'password': 'te$tpwd2'}
        get_user_model().objects.create_user(**data)  # user must exist
        response = self.client.post(SIGNUP_URL, data)
        # asserts
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    @utils.suppress_warnings
    def test_user_create_invalid_password(self):
        """Tests API for new user with invalid password requirements"""
        data = {'email': 'test@email.com', 'password': 'te$tpwd'}
        response = self.client.post(SIGNUP_URL, data)
        # asserts
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


class PrivateUserAPITests(TestCase):
    """Tests User API endpoints for authenticated normal users"""
    def setUp(self):
        """setup api client and sample users and tokens"""
        self.data = {"email": "user@email.com", "password": "norm@lus3r"}
        self.user = samples.sample_user(**self.data)

        self.client = APIClient()
        response = self.client.post(LOGIN_URL, self.data)
        self.token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    @utils.suppress_warnings
    def test_user_create(self):
        """Tests user create API by normal user"""
        data = {'email': 'test2@email.com', 'password': 'te$tpwd2'}
        response = self.client.post(USERS_URL, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @utils.suppress_warnings
    def test_user_list(self):
        """Tests user list API for normal user"""
        response = self.client.get(USERS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_self(self):
        """Tests user detail API of self for normal user"""
        response = self.client.get(get_detail_url(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.user.email)

    @utils.suppress_warnings
    def test_user_detail_other(self):
        """Tests user detail API of other for normal user"""
        other_user = samples.sample_user('test1@email.com', 'te$tpwd1')
        response = self.client.get(get_detail_url(other_user.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update(self):
        """Tests user update API for normal user"""
        data = {
            'email': 'test@email.com',  # update
            'password': self.data.get('password'),
            'first_name': 'Test'
        }
        self.assertEqual(self.user.email, self.data.get('email'))
        self.assertIsNone(self.user.first_name)

        response = self.client.put(get_detail_url(self.user.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), data.get('email'))
        self.assertEqual(response.data.get('first_name'),
                         data.get('first_name'))
        self.assertTrue(self.user.check_password(data.get('password')))

    def test_user_partial_update(self):
        """Tests user partial update API for normal user"""
        data = {
            'email': 'test@email.com',
            'last_name': 'Test',
            'profile': {
                'gender': 'M'
            }
        }
        self.assertEqual(self.user.email, self.data.get('email'))
        self.assertIsNone(self.user.last_name)
        self.assertIsNone(self.user.profile.gender)

        response = self.client.patch(
            get_detail_url(self.user.pk), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), data.get('email'))
        self.assertEqual(response.data.get('last_name'), data.get('last_name'))
        self.assertEqual(response.data['profile']['gender'], "M")


class PrivateStaffAPITests(TestCase):
    """Tests User API endpoints for authenticated staff users"""
    def setUp(self):
        """setup api client and sample users and tokens"""
        self.data = {"email": "staff@email.com", "password": "st@ffus3r"}
        self.user = samples.sample_staffuser(**self.data)

        self.client = APIClient()
        response = self.client.post(LOGIN_URL, self.data)
        self.token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    @utils.suppress_warnings
    def test_user_create(self):
        """Tests user create API by staff user"""
        data = {'email': 'test1@email.com', 'password': 'te$tpwd1'}
        response = self.client.post(USERS_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list(self):
        """Tests user list API for staff user"""
        samples.sample_user('test1@email.com', 'te$tpwd1')
        samples.sample_user('test2@email.com', 'te$tpwd2')
        response = self.client.get(USERS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_user_detail_self(self):
        """Tests user detail API of self for staff user"""
        response = self.client.get(get_detail_url(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.user.email)

    def test_user_detail_other(self):
        """Tests user detail API of other for staff user"""
        other_user = samples.sample_user('test1@email.com', 'te$tpwd1')
        response = self.client.get(get_detail_url(other_user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), other_user.email)

    def test_user_update(self):
        """Tests user update API of other by staff"""
        data = {'email': 'test1@email.com', 'password': 'te$tpwd1'}
        other_user = samples.sample_user(**data)
        self.assertEqual(other_user.email, data.get('email'))
        self.assertIsNone(other_user.first_name)

        data.update({'email': 'test@email.com', 'first_name': 'Test'})
        response = self.client.put(get_detail_url(other_user.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), data.get('email'))
        self.assertEqual(response.data.get('first_name'),
                         data.get('first_name'))
        self.assertTrue(other_user.check_password(data.get('password')))

    def test_user_partial_update(self):
        """Tests user partial update API of other by staff"""
        data = {'email': 'test1@email.com', 'password': 'te$tpwd1'}
        other_user = samples.sample_user(**data)
        self.assertEqual(other_user.email, data.get('email'))
        self.assertIsNone(other_user.last_name)
        self.assertIsNone(self.user.profile.gender)

        data = {
            'email': 'test@email.com',
            'last_name': 'Test',
            'profile': {
                'gender': 'F'
            }
        }
        response = self.client.patch(
            get_detail_url(other_user.pk), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), data.get('email'))
        self.assertEqual(response.data.get('last_name'), data.get('last_name'))
        self.assertEqual(response.data['profile']['gender'], "F")
