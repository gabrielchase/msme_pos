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


class MenuItemViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

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

        self.menu_item_data = {
            'name': 'menu item',
            'description': 'menu item description',
            'price': 80
        }

        self.superuser_data = {
            'email': 'superuser@email.com', 
            'business_name': 'app',
            'identifier': 'admin',
            'owner_surname': 'user',
            'owner_given_name': 'super',
            'password': 'superuser'
        }

        self.superuser = UserProfile.objects.create_superuser(
            email='superuser@email.com', 
            owner_surname='user',
            owner_given_name='super',
            password='superuser'
        )

        self.superuser_login_data = {
            'username': self.superuser_data.get('email'),
            'password': self.superuser_data.get('password')
        }

        self.superuser_client = APIClient()

        self.superuser_api_login_response = self.client.post(
            reverse('api:login-list'),
            self.superuser_login_data,
            format='json'
        )

        self.superuser_login_token = self.superuser_api_login_response.json().get('token')
        self.superuser_client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_login_token)

    def test_api_creates_menu_item_with_logged_in_user(self):
        created_menu_item_response = self.client.post(
            reverse('api:menu_items_create'),
            self.menu_item_data,
            format='json'
        )

        self.assertEqual(created_menu_item_response.status_code, status.HTTP_200_OK)
        self.assertTrue(created_menu_item_response.json().get('id'))
        self.assertTrue(created_menu_item_response.json().get('user_profile'), self.user_data)

    def test_api_cant_create_or_get_menu_items_without_logged_in_user(self):
        no_login_client = APIClient()

        created_menu_item = self.client.post(
            reverse('api:menu_items_create'),
            self.menu_item_data,
            format='json'
        )

        menu_item = MenuItem.objects.get(id=str(created_menu_item.json().get('id')))

        new_menu_item_data = {
            'name': 'updated menu item',
            'description': 'updated menu description',
            'price': 69
        }

        created_menu_item_response = no_login_client.post(
            reverse('api:menu_items_create'),
            self.menu_item_data, 
            format='json'
        )

        get_menu_item_response = no_login_client.get(
            reverse(
                'api:menu_items_detail',
                kwargs={'pk': menu_item.id}
            ),
            format='json'
        )

        updated_menu_item_response = no_login_client.put(
            reverse(
                'api:menu_items_detail', 
                kwargs={'pk': menu_item.id}
            ),
            new_menu_item_data,
            format='json'
        )

        delete_menu_item_response = no_login_client.delete(
            reverse(
                'api:menu_items_detail', 
                kwargs={'pk': menu_item.id}
            ),
            format='json'
        )

        self.assertEqual(created_menu_item_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(get_menu_item_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(updated_menu_item_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_menu_item_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_edit_or_delete_menu_item_as_other_user(self):
        created_menu_item = self.client.post(
            reverse('api:menu_items_create'),
            self.menu_item_data,
            format='json'
        )

        other_client = APIClient()

        other_user_data = {
            'email': 'other_business@email.com', 
            'business_name': 'other_business',
            'identifier': 'other_street',
            'owner_surname': 'test',
            'owner_given_name': 'test',
            'password': 'password',
            'address': '1 street',
            'city': 'city',
            'state': 'state',
        }

        other_user = other_client.post(
            reverse('api:profiles_create'),
            other_user_data,
            format='json'
        ).json()

        other_user_login_data = {
            'username': other_user_data.get('email'),
            'password': other_user_data.get('password')
        }

        api_login_response = other_client.post(
            reverse('api:login-list'),
            other_user_login_data,
            format='json'
        )

        login_token = api_login_response.json().get('token')
        
        other_client.credentials(HTTP_AUTHORIZATION='Token ' + login_token)

        get_menu_item_response = other_client.get(
            reverse(
                'api:menu_items_detail',
                kwargs={'pk': created_menu_item.json().get('id')}
            ),
            format='json'
        )

        update_menu_response = {
            'name': 'other',
            'price': 69
        }

        update_menu_item_response = other_client.put(
            reverse(
                'api:menu_items_detail',
                kwargs={'pk': created_menu_item.json().get('id')}
            ),
            update_menu_response,
            format='json'
        )

        delete_menu_item_response = other_client.delete(
            reverse(
                'api:menu_items_detail',
                kwargs={'pk': created_menu_item.json().get('id')}
            ),
            format='json'
        )

        self.assertEqual(get_menu_item_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(update_menu_item_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_menu_item_response.status_code, status.HTTP_403_FORBIDDEN)

    def only_admin_can_get_all_menu_items(self):
        authenticated_user_api_response = self.client.get(
            reverse('api:menu_items_list'),
            format='json'
        )

        unauthenticated_client = APIClient()

        unauthenticated_client_response = unauthenticated_client.get(
            reverse('api:menu_items_list'),
            format='json'
        ).json()

        superuser_get_menu_list_response = self.superuser_client.get(
            reverse('api:menu_item_list'),
            format='json'
        ).json()

        self.assertEqual(authenticated_user_api_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(unauthenticated_client_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(superuser_get_menu_list_response.status_code, status.HTTP_200_OK)

