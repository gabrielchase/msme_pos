from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from api.models import (
    UserProfile,
    MenuItem
)


class ItemOrderViewSetTestCase(TestCase):
    def setUp(self):
        self.authorized_client = APIClient()
        self.other_authorized_client = APIClient()
        self.unauthorized_client = APIClient()

        self.user_1_data = {
            'email': 'business1@email.com', 
            'business_name': 'business1',
            'identifier': 'street1',
            'owner_surname': 'test1',
            'owner_given_name': 'test1',
            'password': 'password',
            'address': '1 street',
            'city': 'city',
            'state': 'state',
        }

        self.user_1_login_data = {
            'username': self.user_1_data.get('email'),
            'password': self.user_1_data.get('password'),
        }

        self.user_2_data = {
            'email': 'business2@email.com', 
            'business_name': 'business2',
            'identifier': 'street2',
            'owner_surname': 'test2',
            'owner_given_name': 'test2',
            'password': 'password',
            'address': '1 street',
            'city': 'city',
            'state': 'state',
        }

        self.user_2_login_data = {
            'username': self.user_2_data.get('email'),
            'password': self.user_2_data.get('password'),
        }

        self.user_1 = self.unauthorized_client.post(
            reverse('api:profiles_create'),
            self.user_1_data,
            format='json'
        ).json()

        self.user_2 = self.unauthorized_client.post(
            reverse('api:profiles_create'),
            self.user_2_data,
            format='json'
        ).json()

        self.user_1_login_response = self.unauthorized_client.post(
            reverse('api:login-list'),
            self.user_1_login_data,
            format='json'
        )

        self.user_2_login_response = self.unauthorized_client.post(
            reverse('api:login-list'),
            self.user_2_login_data,
            format='json'
        )

        self.user_1_menu_item_1_data = {
            'name': 'user 1 menu item 1',
            'description': 'menu item description 1',
            'price': 80
        }

        self.user_1_menu_item_2_data = {
            'name': 'user 1 menu item 2',
            'description': 'menu item description 2',
            'price': 80
        }

        self.user_2_menu_item_1_data = {
            'name': 'user 2 menu item 1',
            'description': 'menu item description 1',
            'price': 80
        }

        self.user_2_menu_item_2_data = {
            'name': 'user 2 menu item 2',
            'description': 'menu item description 2',
            'price': 80
        }

        self.authorized_client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_login_response.json().get('token'))
        self.other_authorized_client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_login_response.json().get('token'))

        self.user_1_menu_item_1 = self.authorized_client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.user_1.get('full_business_name')}
            ),
            self.user_1_menu_item_1_data,
            format='json'
        ).json()
        
        self.user_1_menu_item_2 = self.authorized_client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.user_1.get('full_business_name')}
            ),
            self.user_1_menu_item_2_data,
            format='json'
        ).json()

        self.user_2_menu_item_1 = self.other_authorized_client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.user_2.get('full_business_name')}
            ),
            self.user_2_menu_item_1_data,
            format='json'
        ).json()

        self.user_2_menu_item_2 = self.other_authorized_client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.user_2.get('full_business_name')}
            ),
            self.user_2_menu_item_2_data,
            format='json'
        ).json()

    def test_setup_successful(self):
        self.assertTrue(self.user_1.get('id'))
        self.assertTrue(self.user_2.get('id'))
        self.assertEqual(self.user_1_login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_2_login_response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_1_menu_item_1.get('id'))
        self.assertTrue(self.user_1_menu_item_2.get('id'))
        self.assertTrue(self.user_2_menu_item_1.get('id'))
        self.assertTrue(self.user_2_menu_item_2.get('id'))



