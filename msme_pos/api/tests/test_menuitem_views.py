from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from api.models import (
    UserProfile,
    MenuItem
)


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

        self.superuser_api_login_response = self.superuser_client.post(
            reverse('api:login-list'),
            self.superuser_login_data,
            format='json'
        )

        self.superuser_login_token = self.superuser_api_login_response.json().get('token')
        self.superuser_client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_login_token)

    def test_api_creates_menu_item_with_logged_in_user(self):
        """ Tests if the  user profile in the created menu item is the 
        same as the user that created the menu item """

        created_menu_item_response = self.client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            self.menu_item_data,
            format='json'
        )

        self.assertEqual(created_menu_item_response.status_code, status.HTTP_200_OK)
        self.assertTrue(created_menu_item_response.json().get('url_param_name'))
        self.assertTrue(created_menu_item_response.json().get('user_profile'), self.user_data)

    def test_api_cant_create_or_get_menu_items_without_logged_in_user(self):
        """ Tests that only logged in users can create, get, update, and delete  menu items """

        no_login_client = APIClient()

        created_menu_item = self.client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            self.menu_item_data,
            format='json'
        )

        menu_item = MenuItem.objects.get(id=created_menu_item.json().get('id'))

        new_menu_item_data = {
            'name': 'updated menu item',
            'description': 'updated menu description',
            'price': 69
        }

        created_menu_item_response = no_login_client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            self.menu_item_data, 
            format='json'
        )

        get_menu_item_response = no_login_client.get(
            reverse(
                'api:menu_items_detail',
                kwargs={
                    'full_business_name': self.created_user.get('full_business_name'),
                    'menu_item_name': menu_item.id
                }
            ),
            format='json'
        )

        updated_menu_item_response = no_login_client.put(
            reverse(
                'api:menu_items_detail', 
                kwargs={
                    'full_business_name': self.created_user.get('full_business_name'),
                    'menu_item_name': menu_item.id
                }
            ),
            new_menu_item_data,
            format='json'
        )

        delete_menu_item_response = no_login_client.delete(
            reverse(
                'api:menu_items_detail', 
                kwargs={
                    'full_business_name': self.created_user.get('full_business_name'),
                    'menu_item_name': menu_item.id
                }
            ),
            format='json'
        )

        self.assertEqual(created_menu_item_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(get_menu_item_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(updated_menu_item_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_menu_item_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_get_edit_or_delete_menu_item_as_other_user(self):
        """ Tests that another user cannot get, edit, or delete another user's menu item """

        created_menu_item = self.client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
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
                kwargs={
                    'full_business_name': other_user.get('full_business_name'),
                    'menu_item_name': created_menu_item.json().get('url_param_name')
                }
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
                kwargs={
                    'full_business_name': other_user.get('full_business_name'),
                    'menu_item_name': created_menu_item.json().get('url_param_name')
                }
            ),
            update_menu_response,
            format='json'
        )


        delete_menu_item_response = other_client.delete(
            reverse(
                'api:menu_items_detail',
                kwargs={
                    'full_business_name': other_user.get('full_business_name'),
                    'menu_item_name': created_menu_item.json().get('url_param_name')
                }
            ),
            format='json'
        )

        self.assertEqual(get_menu_item_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(update_menu_item_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_menu_item_response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_only_admin_can_get_all_menu_items(self):
    #     """ Only an admin/superuser can get all the menu items of another user"""

    #     authenticated_user_api_response = self.client.get(
    #         reverse('api:menu_items_list'),
    #         format='json'
    #     )

    #     unauthenticated_client = APIClient()

    #     unauthenticated_client_response = unauthenticated_client.get(
    #         reverse('api:menu_items_list'),
    #         format='json'
    #     ).json()

    #     superuser_get_menu_list_response = self.superuser_client.get(
    #         reverse('api:menu_item_list'),
    #         format='json'
    #     ).json()

    #     self.assertEqual(authenticated_user_api_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(unauthenticated_client_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(superuser_get_menu_list_response.status_code, status.HTTP_200_OK)

    def test_menu_item_gets_all_orders(self):
        """ Test that the menu item displays all the item orders and that each item order
        has the corresponding id """ 

        menu_item_1_data = {
            'name': 'user 1 menu item 1',
            'description': 'menu item description 1',
            'price': 80
        }

        menu_item_1 = self.client.post(
            reverse(
                'api:menu_items_create',
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            menu_item_1_data,
            format='json'
        )

        self.assertEqual(menu_item_1.status_code, status.HTTP_200_OK)
        self.assertTrue(menu_item_1.json().get('id'))
        
        menu_item_1_order_1_data = {
            'quantity': 1,
            'additional_notes': '111',
            'menu_item': menu_item_1.json()
        }

        menu_item_1_order_2_data = {
            'quantity': 1,
            'additional_notes': '112',
            'menu_item': menu_item_1.json()
        }

        menu_item_1_order_1 = self.client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.created_user.get('full_business_name'),
                    'menu_item_name': menu_item_1.json().get('url_param_name')
                }
            ),
            menu_item_1_order_1_data,
            format='json'
        )

        menu_item_1_order_2 = self.client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.created_user.get('full_business_name'),
                    'menu_item_name': menu_item_1.json().get('url_param_name')
                }
            ),
            menu_item_1_order_2_data,
            format='json'
        )

        self.assertTrue(menu_item_1_order_1.json().get('id'))
        self.assertTrue(menu_item_1_order_2.json().get('id'))
        self.assertEqual(menu_item_1_order_1.status_code, status.HTTP_200_OK)
        self.assertEqual(menu_item_1_order_2.status_code, status.HTTP_200_OK)
        
        get_menu_item_1 = self.client.get(
            reverse(
                'api:menu_items_detail',
                kwargs={
                    'full_business_name': self.created_user.get('full_business_name'),
                    'menu_item_name': menu_item_1.json().get('url_param_name')
                }
            ),
            format='json'
        )

        self.assertEqual(get_menu_item_1.status_code, status.HTTP_200_OK)
        self.assertTrue(get_menu_item_1.json().get('id'))
        self.assertEqual(get_menu_item_1.json().get('name'), menu_item_1.json().get('name'))
        self.assertEqual(get_menu_item_1.json().get('description'), menu_item_1.json().get('description'))
        self.assertEqual(get_menu_item_1.json().get('price'), menu_item_1.json().get('price'))
        self.assertTrue(get_menu_item_1.json().get('item_orders'))
        self.assertTrue(len(get_menu_item_1.json().get('item_orders')), 2)

        get_menu_item_orders = get_menu_item_1.json().get('item_orders')

        self.assertEqual(menu_item_1_order_1.json().get('id'), get_menu_item_orders[0].get('id'))
        self.assertEqual(menu_item_1_order_2.json().get('id'), get_menu_item_orders[1].get('id'))

        self.assertEqual(get_menu_item_orders[0].get('quantity'), menu_item_1_order_1_data.get('quantity'))
        self.assertEqual(get_menu_item_orders[0].get('additional_notes'), menu_item_1_order_1_data.get('additional_notes'))
        self.assertEqual(get_menu_item_orders[0].get('menu_item'), menu_item_1.json().get('id'))

        self.assertEqual(get_menu_item_orders[1].get('quantity'), menu_item_1_order_2_data.get('quantity'))
        self.assertEqual(get_menu_item_orders[1].get('additional_notes'), menu_item_1_order_2_data.get('additional_notes'))
        self.assertEqual(get_menu_item_orders[1].get('menu_item'), menu_item_1.json().get('id'))


