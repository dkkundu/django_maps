"""Core > tests > views > test_user.py"""
# PYTHON IMPORTS
from http import HTTPStatus
# DJANGO IMPORTS
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse
# CORE IMPORTS
from Core.tests.samples import (
    sample_user, sample_staffuser, sample_superuser, get_perm
)
from Core.tests.utils import suppress_warnings


USER_MODEL = get_user_model()
LOGIN_URL = settings.LOGIN_URL

USER_LIST_URL = reverse('core:users')
USER_LIST_PERM = 'Core.view_user'

USER_CREATE_URL = reverse('core:user_create')
USER_CREATE_PERM = 'Core.add_user'


def get_detail_url(pk):
    """Returns detail url"""
    return reverse('core:user_detail', kwargs={'pk': pk})


def get_update_url(pk):
    """Returns update url"""
    return reverse('core:user_update', kwargs={'pk': pk})


class UserListPublicTests(TestCase):
    """Tests User List View for anonymous users"""
    def setUp(self):
        """setup"""
        self.client = Client()

    def test_public_view(self):
        """Tests that anonymous user is redirected to login"""
        response = self.client.get(USER_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302 FOUND

        response = self.client.get(USER_LIST_URL, follow=True)
        self.assertEqual(response.wsgi_request.path, LOGIN_URL)  # redirected
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK


class UserListPrivateTests(TestCase):
    """Tests User List View for authenticated users w/wo permissions"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.staffuser = sample_staffuser()
        self.superuser = sample_superuser()
        self.client = Client()
        self.client.login(email='user@sample.com', password='samplepwd')

    @suppress_warnings
    def test_non_staff_view(self):
        """Tests for user who is not staff"""
        response = self.client.get(USER_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

    @suppress_warnings
    def test_staff_no_permission(self):
        """Tests for user who is staff but no permission to view"""
        self.client.login(email='staff@email.com', password='staffpass')
        self.assertFalse(self.staffuser.has_perm(USER_LIST_PERM))

        response = self.client.get(USER_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403
        self.assertFalse(response.wsgi_request.user.has_perm(USER_LIST_PERM))

    def test_staff_with_permission(self):
        """Tests for user who is staff and has permission to view"""
        self.staffuser.user_permissions.add(
            Permission.objects.get(name='Can view user')
        )
        self.staffuser.full_clean()
        self.staffuser.save()
        self.assertTrue(self.staffuser.has_perm(USER_LIST_PERM))

        self.client.login(email='staff@email.com', password='staffpass')

        response = self.client.get(USER_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertTrue(response.wsgi_request.user.has_perm(USER_LIST_PERM))

    def test_superuser_view(self):
        """Tests user list view for superuser"""
        self.client.login(email='super@email.com', password='superpass')

        response = self.client.get(USER_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK


class UserDetailPublicTests(TestCase):
    """Tests User Detail View for anonymous users"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.client = Client()

    def test_public_view(self):
        """Tests that anonymous user is redirected to login"""
        url = get_update_url(self.user.pk)
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={url}",
            HTTPStatus.FOUND, HTTPStatus.OK
        )  # should redirect to login


class UserDetailPrivateTests(TestCase):
    """Tests User Detail View for authenticated users w/wo permissions"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.otheruser = sample_user(
            email='other@sample.com', password='pass'
        )

        self.staffuser = sample_staffuser()
        self.staffuser.user_permissions.add(
            get_perm('view', 'user'), get_perm('view', 'profile')
        )

        self.otherstaffuser = sample_staffuser(
            email='otherstaff@email.com', password='pass'
        )
        self.otherstaffuser.user_permissions.add(
            get_perm('view', 'user'), get_perm('view', 'profile')
        )

        self.superuser = sample_superuser()
        self.client = Client()
        self.client.login(
            email='user@sample.com', password='samplepwd'
        )

    @suppress_warnings
    def test_user_view_own_profile(self):
        """Tests a normal user cannot view own detail page"""
        url = get_detail_url(self.user.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

    @suppress_warnings
    def test_user_view_other_profile(self):
        """Tests a normal user cannot view other detail page"""
        url = get_detail_url(self.otheruser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

        url = get_detail_url(self.staffuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

        url = get_detail_url(self.superuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

    def test_staffuser_view_own_profile(self):
        """Tests a staffuser can view own detail page"""
        self.client.login(email='staff@email.com', password='staffpass')

        url = get_detail_url(self.staffuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

    @suppress_warnings
    def test_staffuser_view_other_profile(self):
        """Tests a staffuser can view other staff detail page"""
        self.client.login(email='staff@email.com', password='staffpass')

        url = get_detail_url(self.user.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK

        url = get_detail_url(self.otheruser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK

        url = get_detail_url(self.otherstaffuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK

        url = get_detail_url(self.superuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK

    def test_superuser_view_own_profile(self):
        """Tests a superuser can view own detail page"""
        self.client.login(email='super@email.com', password='superpass')

        url = get_detail_url(self.superuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

    def test_superuser_view_other_profile(self):
        """Tests a superuser can view others update page"""
        self.client.login(email='super@email.com', password='superpass')

        url = get_detail_url(self.user.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

        url = get_detail_url(self.staffuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200


class UserCreatePublicTests(TestCase):
    """Tests User Create View for anonymous users"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.client = Client()

    def test_public_view(self):
        """Tests that anonymous user is redirected to login"""
        response = self.client.get(USER_CREATE_URL, follow=True)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={USER_CREATE_URL}",
            HTTPStatus.FOUND, HTTPStatus.OK
        )  # should redirect to login
        response = self.client.post(USER_CREATE_URL, follow=True)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={USER_CREATE_URL}",
            HTTPStatus.FOUND, HTTPStatus.OK
        )  # should redirect to login


class UserCreatePrivateTests(TestCase):
    """Tests User Create View for authenticated users w/wo permissions"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.staffuser = sample_staffuser()
        self.staffuser.user_permissions.add(get_perm('add', 'user'))
        self.superuser = sample_superuser()
        self.client = Client()
        self.client.login(
            email='user@sample.com', password='samplepwd'
        )

    @suppress_warnings
    def test_user_create_view(self):
        """Tests a normal user cannot view create user page"""
        response = self.client.get(USER_CREATE_URL, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403
        response = self.client.post(USER_CREATE_URL, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

    def test_staffuser_create_view(self):
        """Tests a staffuser can view create user page"""
        self.client.login(email='staff@email.com', password='staffpass')

        response = self.client.get(USER_CREATE_URL, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        response = self.client.post(USER_CREATE_URL, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

    def test_superuser_create_view(self):
        """Tests a superuser can view create user page"""
        self.client.login(email='super@email.com', password='superpass')

        response = self.client.get(USER_CREATE_URL, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        response = self.client.post(USER_CREATE_URL, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

    def test_post_valid(self):
        """Tests user create with valid post data"""
        self.client.login(email='super@email.com', password='superpass')

        data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@email.com',
            'password1': 'mnbvcXz@1',
            'password2': 'mnbvcXz@1',
        }

        response = self.client.post(USER_CREATE_URL, data=data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
        self.assertRedirects(
            response, get_detail_url(
                USER_MODEL.objects.get(email='validuser@email.com').pk
            ), HTTPStatus.FOUND, HTTPStatus.OK
        )

    def test_post_invalid(self):
        """Tests user create with invalid post data"""
        self.client.login(email='super@email.com', password='superpass')

        data = {
            'first_name': 'Invalid',
            'last_name': 'User',
            'email': 'invaliduser',
            'password1': 'mnbvcXz@1',
            'password2': 'mnbvcXz@2',
        }

        response = self.client.post(USER_CREATE_URL, data=data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK


class UserUpdatePublicTests(TestCase):
    """Tests User Update View for anonymous users"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.client = Client()

    def test_public_view(self):
        """Tests that anonymous user is redirected to login"""
        url = get_update_url(self.user.pk)
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={url}",
            HTTPStatus.FOUND, HTTPStatus.OK
        )  # should redirect to login
        response = self.client.post(url, follow=True)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={url}",
            HTTPStatus.FOUND, HTTPStatus.OK
        )  # should redirect to login


class UserUpdatePrivateTests(TestCase):
    """Tests User Update View for authenticated users w/wo permissions"""
    def setUp(self):
        """setup"""
        self.user = sample_user()
        self.otheruser = sample_user(
            email='other@sample.com', password='pass'
        )

        self.staffuser = sample_staffuser()
        self.staffuser.user_permissions.add(
            get_perm('view', 'user'), get_perm('change', 'user'),
            get_perm('view', 'profile'), get_perm('change', 'profile')
        )

        self.otherstaffuser = sample_staffuser(
            email='otherstaff@email.com', password='pass'
        )
        self.otherstaffuser.user_permissions.add(
            get_perm('view', 'user'), get_perm('change', 'user'),
            get_perm('view', 'profile'), get_perm('change', 'profile')
        )

        self.superuser = sample_superuser()
        self.client = Client()
        self.client.login(
            email='user@sample.com', password='samplepwd'
        )

    @suppress_warnings
    def test_user_view_own_profile(self):
        """Tests a normal user cannot view own update page"""
        url = get_update_url(self.user.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

    @suppress_warnings
    def test_user_view_other_profile(self):
        """Tests a normal user cannot view other update page"""
        url = get_update_url(self.otheruser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

        url = get_update_url(self.staffuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

        url = get_update_url(self.superuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

    def test_staffuser_view_own_profile(self):
        """Tests a staffuser can view own update page"""
        self.client.login(email='staff@email.com', password='staffpass')

        url = get_update_url(self.staffuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

    @suppress_warnings
    def test_staffuser_view_other_profile(self):
        """Tests a staffuser cannot view other staff update page"""
        self.client.login(email='staff@email.com', password='staffpass')

        url = get_update_url(self.user.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

        url = get_update_url(self.otheruser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

        url = get_update_url(self.otherstaffuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

        url = get_update_url(self.superuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

    def test_superuser_view_own_profile(self):
        """Tests a superuser can view own update page"""
        self.client.login(email='super@email.com', password='superpass')

        url = get_update_url(self.superuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

    def test_superuser_view_other_profile(self):
        """Tests a superuser can view others update page"""
        self.client.login(email='super@email.com', password='superpass')

        url = get_update_url(self.user.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

        url = get_update_url(self.staffuser.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200

    def test_post_valid(self):
        """Tests user update with valid post data"""
        self.client.login(email='super@email.com', password='superpass')

        data = {
            'first_name': 'Staff',
            'last_name': 'User',
            'gender': 'F',
            'passport': 'PA3456789',
            'nid': '1234567890',
        }

        url = get_update_url(self.otherstaffuser.pk)
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK

    def test_post_invalid(self):
        """Tests user update with invalid post data"""
        self.client.login(email='super@email.com', password='superpass')

        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'passport': '123456789',
            'nid': '12345678901',
        }

        url = get_update_url(self.otheruser.pk)
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200 OK
