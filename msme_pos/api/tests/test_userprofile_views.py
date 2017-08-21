from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from api.models import (
    UserProfile,
    UserProfileManager,
    MenuItem
)

manager = UserProfileManager()


class UserProfileViewSetTestCase(TestCase):
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
            reverse('api:profiles_create'),
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


        self.superuser_client = APIClient()

        self.superuser = UserProfile.objects.create_superuser(
            email='superuser@test.com',
            owner_surname='superuser',
            owner_given_name='superuser',
            password='password'
        )

        self.superuser_login_data = {
            'username': self.superuser.email,
            'password': 'password'
        }

        self.superuser_api_login_response = self.superuser_client.post(
            reverse('api:login-list'),
            self.superuser_login_data,
            format='json'
        )

        self.superuser_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.superuser_api_login_response.json().get('token')
        )

        self.unauthenticated_client = APIClient()

    def test_api_can_create_user(self):
        """ New users can be created and are not superuser or staff """

        new_count = UserProfile.objects.count()

        self.assertNotEqual(self.old_count, new_count)
        self.assertEqual(self.api_response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.api_response.json().get('is_superuser'))
        self.assertFalse(self.api_response.json().get('is_staff'))

    def test_api_can_get_user_list(self):
        """ Test that only superusers can get a list of all users """

        unauthenticated_client = APIClient()

        authenticated_api_response = self.client.get(
            reverse('api:profiles_list'),
            format='json'
        )

        unauthenticated_api_response = unauthenticated_client.get(
            reverse('api:profiles_list'),
            format='json'
        )

        superuser_api_response = self.superuser_client.get(
            reverse('api:profiles_list'),
            format='json'
        )

        self.assertEqual(authenticated_api_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(authenticated_api_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(superuser_api_response.status_code, status.HTTP_200_OK)

    def test_api_can_get_user(self):
        """ Test that anly a user or superuser can get their own profile """

        api_response = self.client.get(
            reverse(
                'api:profiles_detail', 
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            format='json'
        )

        superuser_api_response = self.superuser_client.get(
            reverse(
                'api:profiles_detail', 
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            format='json'
        )

        other_client = APIClient()

        unauthenticated_api_response = self.unauthenticated_client.get(
            reverse(
                'api:profiles_detail', 
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

        self.assertEqual(unauthenticated_api_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(superuser_api_response.status_code, status.HTTP_200_OK)

    def test_api_can_update_user(self):
        """ Test that a user can update their attributes """

        user_to_be_updated = UserProfile.objects.get(email=self.created_user.get('email'))

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
                'api:profiles_detail', 
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
        """ Test that a user account can be deleted """

        user_to_be_deleted = UserProfile.objects.get(email=self.created_user.get('email'))

        api_response = self.client.delete(
            reverse(
                'api:profiles_detail', 
                kwargs={'full_business_name': user_to_be_deleted.full_business_name}
            ),
            format='json'
        )
        
        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_cannot_update_without_token(self):
        """ Test that another user can't update another users attributes """

        no_token_client = APIClient()
        user_to_be_updated = UserProfile.objects.get(email=self.created_user.get('email'))

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
                'api:profiles_detail', 
                kwargs={'full_business_name': user_to_be_updated.full_business_name}
            ),
            new_user_data,
            format='json'
        )

        self.assertEqual(api_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_cannot_delete_without_token(self):
        no_token_client = APIClient()
        user_to_be_deleted = UserProfile.objects.get(email=self.created_user.get('email'))

        api_response = no_token_client.delete(
            reverse(
                'api:profiles_detail', 
                kwargs={'full_business_name': user_to_be_deleted.full_business_name}
            ),
            format='json'
        )
        
        self.assertEqual(api_response.status_code, status.HTTP_401_UNAUTHORIZED)
