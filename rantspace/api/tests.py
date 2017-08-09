from django.test import TestCase
from django.db import IntegrityError

from api.models import (
    UserProfile,
    UserProfileManager
)


manager = UserProfileManager()
# UserProfile = UserProfile()

class ModelTestCase(TestCase):
    def setUp(self):
        self.old_count = UserProfile.objects.count()

        self.user_attributes = {
            'email': 'test@test.com', 
            'surname': 'test',
            'given_name': 'test',
            'password': 'password'
        }
        
        UserProfile.objects.create_user(
            email=self.user_attributes.get('email'),
            surname=self.user_attributes.get('surname'),
            given_name=self.user_attributes.get('given_name'),
            password=self.user_attributes.get('password')
        )

    def test_model_saves_user(self):
        new_count = UserProfile.objects.count()
        new_user = UserProfile.objects.get(email='test@test.com')

        self.assertNotEqual(self.old_count, new_count)
        self.assertEqual(bool(new_user.id), True)
        self.assertEqual(new_user.email, self.user_attributes.get('email'))
        self.assertNotEqual(new_user.password, self.user_attributes.get('password'))
        self.assertEqual(new_user.surname, self.user_attributes.get('surname'))
        self.assertEqual(new_user.given_name, self.user_attributes.get('given_name'))
        self.assertEqual(new_user.is_active, True)
        self.assertEqual(new_user.is_staff, False)


    def test_model_normalizes_email(self):
        normalize_email_attributes = {
            'email': 'test@TeSt2.cOm', 
            'surname': 'test',
            'given_name': 'test',
            'password': 'password'
        }

        user = UserProfile.objects.create_user(
            email=normalize_email_attributes.get('email'),
            surname=normalize_email_attributes.get('surname'),
            given_name=normalize_email_attributes.get('given_name'),
            password=normalize_email_attributes.get('password')
        )

        self.assertEqual(user.email, 'test@test2.com')

    def test_model_raises_error_when_email_not_provided(self):
        no_email_attributes = {
            'surname': 'test',
            'given_name': 'test',
            'password': 'password'
        }

        with self.assertRaises(ValueError) as context:
            UserProfile.objects.create_user(
                email=None,
                surname=no_email_attributes.get('surname'),
                given_name=no_email_attributes.get('given_name'),
                password=no_email_attributes.get('password')
            )

            self.assertTrue('Users must provide an email address' in context.exception)

    def test_model_create_superuser(self):
        superuser_email = 'superuser@test.com'

        superuser = UserProfile.objects.create_superuser(
            email=superuser_email,
            surname=self.user_attributes.get('surname'),
            given_name=self.user_attributes.get('given_name'),
            password=self.user_attributes.get('password')
        )

        self.assertEqual(bool(superuser.id), True)
        self.assertEqual(superuser.email, superuser_email)
        self.assertNotEqual(superuser.password, self.user_attributes.get('password'))
        self.assertEqual(superuser.surname, self.user_attributes.get('surname'))
        self.assertEqual(superuser.given_name, self.user_attributes.get('given_name'))
        self.assertEqual(superuser.is_active, True)
        self.assertEqual(superuser.is_staff, True)
        self.assertEqual(superuser.is_superuser, True)

    def test_model_raise_duplicate_user_error(self):
        with self.assertRaises(IntegrityError) as context:
            UserProfile.objects.create_user(
                email=self.user_attributes.get('email'),
                surname=self.user_attributes.get('surname'),
                given_name=self.user_attributes.get('given_name'),
                password=self.user_attributes.get('password')
            )

            self.assertTrue('duplicate key value violates unique constraint' in context.exception)
