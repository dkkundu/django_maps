"""API > tests > views > test_profile.py"""
# PYTHON IMPORTS
import io
import os
import tempfile
from PIL import Image
# DJANGO IMPORTS
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
# DRF IMPORTS
from rest_framework import status
from rest_framework.test import APIClient
# CORE IMPORTS
from Core.tests import samples, utils


def get_image_upload_url(pk):
    """Return user detail url"""
    return reverse('api:profile-image', args=[pk])


def generate_image_file():
    """returns a dummy image file"""
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(1, 2, 3))
    image.save(file, 'png')
    file.name = 'django_api_test_image.png'
    file.seek(0)
    return file


class PublicImageUploadAPITests(TestCase):
    """Tests API for non-authenticated requests on image upload endpoint"""
    def setUp(self):
        """setup the client"""
        self.media_dir = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = tempfile.gettempdir()
        self.image_file = generate_image_file()

        self.data = {"email": "profile@email.com", "password": "norm@lus3r"}
        self.user = samples.sample_user(**self.data)
        self.client = APIClient()

    @utils.suppress_warnings
    def test_get_image(self):
        """Tests API for retrieving image for user profile"""
        response = self.client.get(get_image_upload_url(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @utils.suppress_warnings
    def test_patch_image(self):
        """Tests API for patching image for user profile"""
        response = self.client.patch(
            get_image_upload_url(self.user.pk), {'image': self.image_file}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @utils.suppress_warnings
    def test_put_image(self):
        """Tests API for putting image for user profile"""
        response = self.client.put(
            get_image_upload_url(self.user.pk), {'image': self.image_file}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        """Reset settings and delete temporary files"""
        settings.MEDIA_ROOT = self.media_dir


class PrivateImageUploadAPITests(TestCase):
    """Tests API for authenticated requests on image upload endpoint"""
    def setUp(self):
        """setup the client"""
        self.media_dir = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = tempfile.gettempdir()
        self.image_file = generate_image_file()

        self.data = {"email": "profile@email.com", "password": "norm@lus3r"}
        self.user = samples.sample_user(**self.data)
        self.client = APIClient()
        response = self.client.post(reverse('api:auth-login'), self.data)
        self.token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_get_image(self):
        """Tests API for retrieving image for user profile"""
        response = self.client.get(get_image_upload_url(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)

    def test_patch_image(self):
        """Tests API for patching image for user profile"""
        response = self.client.patch(
            get_image_upload_url(self.user.pk),
            data={'image': self.image_file}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filename = response.data.get('image').split("/media/")[-1]
        path = os.path.join(settings.MEDIA_ROOT, filename)
        self.assertTrue(os.path.exists(path))
        if os.path.exists(path):
            os.remove(path)

    def test_put_image(self):
        """Tests API for putting image for user profile"""
        response = self.client.put(  # user id = 1
            get_image_upload_url(self.user.pk),
            data={'image': self.image_file}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filename = response.data.get('image').split("/media/")[-1]
        path = os.path.join(settings.MEDIA_ROOT, filename)
        self.assertTrue(os.path.exists(path))
        if os.path.exists(path):
            os.remove(path)

    def tearDown(self):
        """Reset settings and delete temporary files"""
        settings.MEDIA_ROOT = self.media_dir
