"""Core > tests > models > test_profile.py"""
# PYTHON IMPORTS
import os
import shutil
# DJANGO IMPORTS
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
# CORE IMPORTS
from Core.models import Profile
from Core.tests.samples import sample_user


class ProfileTests(TestCase):
    """Test class for Profile model"""

    def test_profile_create_signal(self):
        """Tests if a profile is created on user creation"""
        user = sample_user()
        profile = Profile.objects.get(user=user)

        # assert
        self.assertEqual(profile, user.profile)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.user.email, user.email)

    def test_profile_update_signal(self):
        """Tests if a profile is updated on user update"""
        user = sample_user()
        user.first_name = 'First'
        user.last_name = 'Last'
        user.profile.gender = 'M'
        user.full_clean()
        user.save()

        profile = Profile.objects.get(user=user)

        # assert
        self.assertEqual(profile.gender, 'M')
        self.assertEqual(profile.user.get_full_name(), 'First Last')

    def test_profile_str(self):
        """Tests string representation of Profile"""
        user = sample_user('someone@email.net', 'password')
        profile = Profile.objects.get(user=user)

        # assert
        self.assertEqual(str(profile), profile.user.email)

    def test_profile_age(self):
        """Tests a user's age in Profile"""
        user = sample_user()
        self.assertIsNone(user.profile.birthday)
        self.assertEqual(user.profile.age, 0)

        user.profile.birthday = timezone.datetime(1988, 5, 19)
        user.full_clean()
        user.save()

        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile.birthday)
        self.assertEqual(
            int((timezone.now().date() - profile.birthday).days / 365.25),
            profile.age
        )

    @override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'tmp'))
    def test_profile_picture(self):
        """Tests a user's profile picture upload"""
        user = sample_user()
        profile = Profile.objects.get(user=user)
        profile.image = SimpleUploadedFile(
            'profile_pic.jpg', b'this is a profile picture', 'image/jpeg'
        )
        profile.full_clean()
        profile.save()

        # assert
        self.assertIsNotNone(profile.image)
        self.assertTrue(os.path.exists(profile.image.file.name))
        self.assertEqual(  # test for upload path
            profile.image.name,
            f"Users/{profile.user.id}/{profile.image.name.split('/')[-1]}"
        )
        profile.image.close()

    def tearDown(self):
        """cleanup"""
        tmp_dir = os.path.join(settings.BASE_DIR, 'tmp')
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
