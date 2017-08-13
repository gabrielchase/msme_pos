from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from rest_framework import status
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
        self.assertEqual(str(new_user), new_user.get_full_name())

    def test_model_saves_user(self):
        new_count = UserProfile.objects.count()
        new_user = UserProfile.objects.get(email='business@email.com')

        self.assertNotEqual(self.old_count, new_count)
        self.assertEqual(bool(new_user.id), True)
        self.assertEqual(new_user.email, self.user_attributes.get('email'))
        self.assertEqual(new_user.business_name, self.user_attributes.get('business_name'))
        self.assertEqual(new_user.identifier, self.user_attributes.get('identifier'))
        self.assertEqual(new_user.full_business_name, new_user.get_full_name())
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
        self.assertEqual(superuser.full_business_name, superuser.get_full_name())
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
            business_name='null-values',
            identifier='1',
            owner_surname=self.user_attributes.get('owner_surname'),
            owner_given_name=self.user_attributes.get('owner_given_name'),
            password=self.user_attributes.get('password')
        )

        new_count = UserProfile.objects.count()

        self.assertNotEqual(self.old_count, new_count)
        self.assertEqual(user.address, None)
        self.assertEqual(user.city, None)
        self.assertEqual(user.state, None)


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


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.old_count = UserProfile.objects.count()

        self.user_data = {
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

        self.api_response = self.client.post(
            reverse('api:profile-list'),
            self.user_data,
            format='json'
        )

        self.created_user = self.api_response.json()

        self.user_login_data = {
            'username': self.user_data.get('email'),
            'password': self.user_data.get('password'),
        }

        self.api_login_response = self.client.post(
            reverse('api:login-list'),
            self.user_login_data,
            format='json'
        )

        self.login_token = self.api_login_response.json().get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.login_token)


    def test_api_can_create_user(self):
        new_count = UserProfile.objects.count()

        self.assertNotEqual(self.old_count, new_count)
        self.assertEqual(self.api_response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.api_response.json().get('is_superuser'))
        self.assertFalse(self.api_response.json().get('is_staff'))

    def test_api_can_get_user_list(self):
        self.api_response = self.client.get(
            reverse('api:profile-list'),
            format='json'
        )

        self.assertTrue(self.api_response.json())

        for user in self.api_response.json():
            self.assertTrue(user.get('id'))

    def test_api_can_get_user(self):
        api_response = self.client.get(
            reverse(
                'api:profile-detail', 
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            format='json'
        )

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertTrue(api_response.json().get('id'))
        self.assertEqual(api_response.json().get('email'), self.created_user.get('email'))
        self.assertEqual(api_response.json().get('business_name'), self.created_user.get('business_name'))
        self.assertEqual(api_response.json().get('identifier'), self.created_user.get('identifier'))
        self.assertEqual(api_response.json().get('full_business_name'), '{}-{}'.format(self.created_user.get('business_name'), self.created_user.get('identifier')))
        self.assertEqual(api_response.json().get('owner_surname'), self.created_user.get('owner_surname'))
        self.assertEqual(api_response.json().get('owner_given_name'), self.created_user.get('owner_given_name'))
        self.assertFalse(api_response.json().get('is_superuser'))
        self.assertFalse(api_response.json().get('is_staff'))

    def test_api_can_update_user(self):
        user_to_be_updated = UserProfile.objects.get()

        new_user_data = {
            'email': 'business_email_2@email.com',
            'password': user_to_be_updated.password,
            'business_name': 'business2',
            'identifier': 'street2',
            'owner_surname': 'owner2',
            'owner_given_name': 'owner2',
            'address': 'address2',
            'city': 'city2',
            'state': 'state2'
        }

        api_response = self.client.put(
            reverse(
                'api:profile-detail', 
                kwargs={'full_business_name': user_to_be_updated.full_business_name}
            ),
            new_user_data,
            format='json'
        )

        updated_user = api_response.json()

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.get('id'), user_to_be_updated.id)
        self.assertEqual(updated_user.get('email'), new_user_data.get('email'))
        self.assertNotEqual(updated_user.get('password'), new_user_data.get('password'))
        self.assertEqual(updated_user.get('business_name'), new_user_data.get('business_name'))
        self.assertEqual(updated_user.get('identifier'), new_user_data.get('identifier'))
        self.assertEqual(updated_user.get('full_business_name'), '{}-{}'.format(new_user_data.get('business_name'), new_user_data.get('identifier')))
        self.assertEqual(updated_user.get('owner_surname'), new_user_data.get('owner_surname'))
        self.assertEqual(updated_user.get('owner_given_name'), new_user_data.get('owner_given_name'))
        self.assertEqual(updated_user.get('address'), new_user_data.get('address'))
        self.assertEqual(updated_user.get('city'), new_user_data.get('city'))
        self.assertEqual(updated_user.get('state'), new_user_data.get('state'))

    def test_api_can_delete_user(self):
        user_to_be_deleted = UserProfile.objects.get()

        api_response = self.client.delete(
            reverse(
                'api:profile-detail', 
                kwargs={'full_business_name': user_to_be_deleted.full_business_name}
            ),
            format='json'
        )
        
        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_cannot_update_without_token(self):
        no_token_client = APIClient()
        user_to_be_updated = UserProfile.objects.get()

        new_user_data = {
            'email': 'business_email_2@email.com',
            'password': user_to_be_updated.password,
            'business_name': 'business2',
            'identifier': 'street2',
            'owner_surname': 'owner2',
            'owner_given_name': 'owner2',
            'address': 'address2',
            'city': 'city2',
            'state': 'state2'
        }

        api_response = no_token_client.put(
            reverse(
                'api:profile-detail', 
                kwargs={'full_business_name': user_to_be_updated.full_business_name}
            ),
            new_user_data,
            format='json'
        )

        self.assertEqual(api_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_cannot_delete_without_token(self):
        no_token_client = APIClient()
        user_to_be_deleted = UserProfile.objects.get()

        api_response = no_token_client.delete(
            reverse(
                'api:profile-detail', 
                kwargs={'full_business_name': user_to_be_deleted.full_business_name}
            ),
            format='json'
        )
        
        self.assertEqual(api_response.status_code, status.HTTP_401_UNAUTHORIZED)
