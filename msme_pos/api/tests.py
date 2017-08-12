from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from rest_framework.test import APIClient

from api.models import (
    UserProfile,
    UserProfileManager
)


manager = UserProfileManager()


class ModelTestCase(TestCase):
    def setUp(self):
        self.old_count = UserProfile.objects.count()

        self.user_attributes = {
            'email': 'business@email.com', 
            'business_name': 'business',
            'identifier': 'street',
            'owner_surname': 'test',
            'owner_given_name': 'test',
            'password': 'password',
            'address': '1 street',
            'city': 'city',
            'state': 'state',
        }
        
        UserProfile.objects.create_user(
            email=self.user_attributes.get('email'),
            business_name=self.user_attributes.get('business_name'),
            identifier=self.user_attributes.get('identifier'),
            owner_surname=self.user_attributes.get('owner_surname'),
            owner_given_name=self.user_attributes.get('owner_given_name'),
            password=self.user_attributes.get('password'),
            address=self.user_attributes.get('address'),
            city=self.user_attributes.get('city'),
            state=self.user_attributes.get('state'),
        )

    def test_model_saves_user(self):
        new_count = UserProfile.objects.count()
        new_user = UserProfile.objects.get(email='business@email.com')

        self.assertNotEqual(self.old_count, new_count)
        self.assertEqual(bool(new_user.id), True)
        self.assertEqual(new_user.email, self.user_attributes.get('email'))
        self.assertEqual(new_user.business_name, self.user_attributes.get('business_name'))
        self.assertEqual(new_user.identifier, self.user_attributes.get('identifier'))
        self.assertNotEqual(new_user.password, self.user_attributes.get('password'))
        self.assertEqual(new_user.owner_surname, self.user_attributes.get('owner_surname'))
        self.assertEqual(new_user.owner_given_name, self.user_attributes.get('owner_given_name'))
        self.assertEqual(new_user.address, self.user_attributes.get('address'))
        self.assertEqual(new_user.city, self.user_attributes.get('city'))
        self.assertEqual(new_user.state, self.user_attributes.get('state'))
        self.assertEqual(new_user.is_active, True)
        self.assertEqual(new_user.is_staff, False)


    def test_model_normalizes_email(self):
        normalize_email_attributes = {
            'email': 'test@TeSt2.cOm', 
            'business_name': 'business',
            'identifier': 'identifier',
            'owner_surname': 'test',
            'owner_given_name': 'test',
            'password': 'password'
        }

        user = UserProfile.objects.create_user(
            email=normalize_email_attributes.get('email'),
            business_name=normalize_email_attributes.get('business_name'),
            identifier=normalize_email_attributes.get('identifier'),
            owner_surname=normalize_email_attributes.get('owner_surname'),
            owner_given_name=normalize_email_attributes.get('owner_given_name'),
            password=normalize_email_attributes.get('password')
        )

        self.assertEqual(user.email, 'test@test2.com')

    def test_model_raises_error_when_email_not_provided(self):
        no_email_attributes = {
            'business_name': 'business',
            'identifier': 'identifier',
            'owner_surname': 'test',
            'owner_given_name': 'test',
            'password': 'password'
        }

        with self.assertRaises(ValueError) as context:
            UserProfile.objects.create_user(
                email=None,
                business_name=no_email_attributes.get('business_name'),
                identifier=no_email_attributes.get('identifier'),
                owner_surname=no_email_attributes.get('owner_surname'),
                owner_given_name=no_email_attributes.get('owner_given_name'),
                password=no_email_attributes.get('password')
            )

            self.assertTrue('Users must provide an email address' in context.exception)

    def test_model_create_superuser(self):
        superuser_email = 'superuser@test.com'

        superuser = UserProfile.objects.create_superuser(
            email=superuser_email,
            owner_surname=self.user_attributes.get('owner_surname'),
            owner_given_name=self.user_attributes.get('owner_given_name'),
            password=self.user_attributes.get('password')
        )

        self.assertEqual(bool(superuser.id), True)
        self.assertEqual(superuser.email, superuser_email)
        self.assertEqual(superuser.business_name, 'app')
        self.assertEqual(superuser.identifier, 'admin')
        self.assertNotEqual(superuser.password, self.user_attributes.get('password'))
        self.assertEqual(superuser.owner_surname, self.user_attributes.get('owner_surname'))
        self.assertEqual(superuser.owner_given_name, self.user_attributes.get('owner_given_name'))
        self.assertEqual(superuser.is_active, True)
        self.assertEqual(superuser.is_staff, True)
        self.assertEqual(superuser.is_superuser, True)

    def test_model_raise_duplicate_user_error(self):
        with self.assertRaises(IntegrityError) as context:
            UserProfile.objects.create_user(
                email=self.user_attributes.get('email'),
                business_name=self.user_attributes.get('business_name'),
                identifier=self.user_attributes.get('identifier'),
                owner_surname=self.user_attributes.get('owner_surname'),
                owner_given_name=self.user_attributes.get('owner_given_name'),
                password=self.user_attributes.get('password')
            )

            self.assertTrue('duplicate key value violates unique constraint' in context.exception)

    def test_model_saves_address_city_state_as_null(self):
        user = UserProfile.objects.create_user(
            email='nullvalues@email.com',   
            business_name=self.user_attributes.get('business_name'),
            identifier=self.user_attributes.get('identifier'),
            owner_surname=self.user_attributes.get('owner_surname'),
            owner_given_name=self.user_attributes.get('owner_given_name'),
            password=self.user_attributes.get('password')
        )

        new_count = UserProfile.objects.count()

        self.assertNotEqual(self.old_count, new_count)
        self.assertEqual(user.address, None)
        self.assertEqual(user.city, None)
        self.assertEqual(user.state, None)

    def test_model_get_short_name(self):
        new_user = UserProfile.objects.get(email='business@email.com')
        self.assertEqual(new_user.get_short_name(), new_user.owner_surname + ', ' + new_user.owner_given_name)
        
    def test_model_get_full_name(self):
        new_user = UserProfile.objects.get(email='business@email.com')
        self.assertEqual(new_user.get_full_name(), new_user.business_name + '-' + new_user.identifier)

    def test_model_get_email(self):
        new_user = UserProfile.objects.get(email='business@email.com')
        self.assertEqual(new_user.get_email(), new_user.email)

    def test_model_str(self):
        new_user = UserProfile.objects.get(email='business@email.com')
        self.assertEqual(str(new_user), new_user.get_full_name() + ': ' + new_user.get_short_name())


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user_attributes = {
            'email': 'business@email.com', 
            'business_name': 'business',
            'identifier': 'street',
            'owner_surname': 'test',
            'owner_given_name': 'test',
            'password': 'password',
            'address': '1 street',
            'city': 'city',
            'state': 'state',
        }
        
        UserProfile.objects.create_user(
            email=self.user_attributes.get('email'),
            business_name=self.user_attributes.get('business_name'),
            identifier=self.user_attributes.get('identifier'),
            owner_surname=self.user_attributes.get('owner_surname'),
            owner_given_name=self.user_attributes.get('owner_given_name'),
            password=self.user_attributes.get('password'),
            address=self.user_attributes.get('address'),
            city=self.user_attributes.get('city'),
            state=self.user_attributes.get('state'),
        )

        self.client = APIClient()

    def test_login_returns_token(self):
        user_data = {
            'username': self.user_attributes.get('email'),
            'password': self.user_attributes.get('password'),
        }

        response = self.client.post(
            reverse('api:login-list'),
            user_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.json())
        self.assertNotEqual(response.json().get('token'), None)
