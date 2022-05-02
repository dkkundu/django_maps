"""Core > tests > test_urls.py"""
# DJANGO IMPORTS
from django.conf import settings
from django.test import TestCase
# CORE IMPORTS
from Core.tests.utils import suppress_warnings


class PublicUrlsTest(TestCase):
    """Test class for testing project URLs in public mode"""

    def test_admin_url(self):
        """Tests public admin panel url"""
        response = self.client.get(f'/{settings.ADMIN_URL}/')
        self.assertEqual(response.status_code, 302)  # redirected to login

    @suppress_warnings
    def test_media_url(self):
        """Tests public media url"""
        response = self.client.get(settings.MEDIA_URL)
        self.assertEqual(response.status_code, 404)  # indexing off

    @suppress_warnings
    def test_debug_url(self):
        """Tests debug toolbar url"""
        response = self.client.get('/__debug__/')
        self.assertEqual(response.status_code, 404)  # needs store-id
