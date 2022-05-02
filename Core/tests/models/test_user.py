"""Core > tests > models > test_user.py"""
# PYTHON IMPORTS
import logging
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
# TESTS IMPORTS
from Core.tests.samples import sample_user
from Core.tests.utils import suppress_errors


USER_MODEL = get_user_model()


class UserModelTest(TestCase):
    """Test Class for User Model"""

    def test_create_user(self):
        """Tests create_user with email address and password"""
        # setup
        email = "admin@ZuBe.dev"
        password = "Admin123#"

        # run
        user = USER_MODEL.objects.create_user(
            email=email,
            password=password
        )

        # assert
        self.assertEqual(user.email, email.lower())  # checks normalization
        self.assertNotEqual(user.password, password)  # checks for plain-text
        self.assertTrue(user.check_password(password))  # checks password

    @suppress_errors
    def test_create_user_with_no_email(self):
        """Tests create_user with no email address provided by user"""
        logging.disable(logging.CRITICAL)  # only critical level log output

        # setup with no email variable
        password = "admin123"

        # run/assert
        with self.assertRaises(AttributeError):  # using email=""
            USER_MODEL.objects.create_user("", password=password)
        with self.assertRaises(AttributeError):  # using email=None
            USER_MODEL.objects.create_user(None, password=password)

        logging.disable(logging.NOTSET)  # reset logging level

    def test_create_user_status(self):
        """Tests create_user staff and superuser status"""
        # setup
        email = "admin@zube.dev"
        password = "notstafforsuperuser"

        # run
        user = USER_MODEL.objects.create_user(email, password)

        # assert
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_staffuser(self):
        """Tests create_staffuser functionality"""
        # setup
        email = "staff@zube.dev"
        password = "staffuser"

        # run
        user = USER_MODEL.objects.create_staffuser(
            email=email,
            password=password
        )

        # assert
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser(self):
        """Tests create_superuser functionality"""
        # setup
        email = "admin@zube.dev"
        password = "superuser"

        # run
        user = USER_MODEL.objects.create_superuser(
            email=email,
            password=password
        )

        # assert
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_user_str(self):
        """Tests string representation of User"""
        # setup
        email = 'someone@email.net'
        user = sample_user(email, 'password')

        # assert
        self.assertEqual(str(user), email)

    def test_user_update(self):
        """Tests user object updating and saving"""
        # setup
        user = sample_user(first_name='Someone')
        self.assertEqual(user.first_name, 'Someone')
        self.assertIsNone(user.last_name)

        # update
        user.first_name = 'Sample'
        user.last_name = 'User'
        user.full_clean()
        user.save()  # updates user

        # assert
        self.assertNotEqual(user.first_name, 'Someone')
        self.assertIsNotNone(user.last_name)
        self.assertEqual(user.first_name, 'Sample')
        self.assertEqual(user.last_name, 'User')

    def test_get_full_name(self):
        """Tests retrieval of user's full name"""
        # test for none
        user = sample_user()
        self.assertIsNone(user.get_full_name())

        # test with first only
        user.first_name = 'First'
        user.full_clean()
        user.save()
        self.assertEqual(user.get_full_name(), 'First')

        # test with last only
        user.first_name = None
        user.last_name = 'Name'
        user.full_clean()
        user.save()
        self.assertEqual(user.get_full_name(), 'Name')

        # test with both first and last name
        user.first_name = 'First'
        user.full_clean()
        user.save()
        self.assertEqual(user.get_full_name(), 'First Name')

    def test_phone_format(self):
        """Tests regex validation of phone field"""
        # setup
        user = sample_user()

        # test minimum length
        with self.assertRaises(ValidationError):
            user.phone = '123456789'
            user.full_clean()
            user.save()

        # test maximum length
        with self.assertRaises(ValidationError):
            user.phone = '0123456789000'
            user.full_clean()
            user.save()

        # test non digits
        with self.assertRaises(ValidationError):
            user.phone = '+123456789O'
            user.full_clean()
            user.save()

        # test valid format
        user.phone = '0123456789'
        user.full_clean()
        user.save()
        self.assertEqual(user.phone, '0123456789')

    def test_get_phone_intl_format(self):
        """Tests international formatted phone number"""
        # setup
        user = sample_user()
        self.assertIsNone(user.get_phone_intl_format())

        user.phone = '01234567890'
        user.full_clean()
        user.save()

        # assert
        self.assertEqual(user.phone, '01234567890')
        self.assertEqual(user.get_phone_intl_format(), '+8801234567890')
        self.assertEqual(
            user.get_phone_intl_format(prefix='+1'), '+101234567890'
        )
