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

        self.user_1_menu_item_1_order_1_data = {
            'quantity': 1,
            'additional_notes': '111',
            'menu_item': self.user_1_menu_item_1
        }

        self.user_1_menu_item_1_order_2_data = {
            'quantity': 1,
            'additional_notes': '112',
            'menu_item': self.user_1_menu_item_1
        }

        self.user_1_menu_item_2_order_1_data = {
            'quantity': 1,
            'additional_notes': '121',
            'menu_item': self.user_1_menu_item_2
        }

        self.user_1_menu_item_2_order_2_data = {
            'quantity': 1,
            'additional_notes': '122',
            'menu_item': self.user_1_menu_item_2
        }

        self.user_2_menu_item_1_order_1_data = {
            'quantity': 1,
            'additional_notes': '211',
            'menu_item': self.user_2_menu_item_1
        }

        self.user_2_menu_item_1_order_2_data = {
            'quantity': 1,
            'additional_notes': '212',
            'menu_item': self.user_2_menu_item_1
        }

        self.user_2_menu_item_2_order_1_data = {
            'quantity': 1,
            'additional_notes': '221',
            'menu_item': self.user_2_menu_item_2
        }

        self.user_2_menu_item_2_order_2_data = {
            'quantity': 1,
            'additional_notes': '222',
            'menu_item': self.user_2_menu_item_2
        }

        self.user_1_menu_item_1_order_1 = self.authorized_client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_1.get('url_param_name')
                }
            ),
            self.user_1_menu_item_1_order_1_data,
            format='json'
        ).json()

        self.user_1_menu_item_1_order_2 = self.authorized_client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_1.get('url_param_name')
                }
            ),
            self.user_1_menu_item_1_order_2_data,
            format='json'
        ).json()

        self.user_1_menu_item_2_order_1 = self.authorized_client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_2.get('url_param_name')
                }
            ),
            self.user_1_menu_item_2_order_1_data,
            format='json'
        ).json()

        self.user_1_menu_item_2_order_2 = self.authorized_client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_2.get('url_param_name')
                }
            ),
            self.user_1_menu_item_2_order_2_data,
            format='json'
        ).json()

        self.user_2_menu_item_1_order_1 = self.authorized_client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_1.get('url_param_name')
                }
            ),
            self.user_2_menu_item_1_order_1_data,
            format='json'
        ).json()

        self.user_2_menu_item_1_order_2 = self.authorized_client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_1.get('url_param_name')
                }
            ),
            self.user_2_menu_item_1_order_2_data,
            format='json'
        ).json()

        self.user_2_menu_item_2_order_1 = self.authorized_client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_2.get('url_param_name')
                }
            ),
            self.user_2_menu_item_2_order_1_data,
            format='json'
        ).json()

        self.user_2_menu_item_2_order_2 = self.authorized_client.post(
            reverse(
                'api:item_order_create',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_2.get('url_param_name')
                }
            ),
            self.user_2_menu_item_2_order_2_data,
            format='json'
        ).json()

    def test_setup_successful(self):
        """ Test that the users have  been created"""
        self.assertTrue(self.user_1.get('id'))
        self.assertTrue(self.user_2.get('id'))

        """ Test that both the users can login """
        self.assertEqual(self.user_1_login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_2_login_response.status_code, status.HTTP_200_OK)

        """ Test that all menu items are created """
        self.assertTrue(self.user_1_menu_item_1.get('id'))
        self.assertTrue(self.user_1_menu_item_2.get('id'))
        self.assertTrue(self.user_2_menu_item_1.get('id'))
        self.assertTrue(self.user_2_menu_item_2.get('id'))

        """ Test that each menu item was created by their respective user"""
        self.assertEqual(self.user_1_menu_item_1.get('user_profile'), self.user_1.get('id'))
        self.assertEqual(self.user_1_menu_item_2.get('user_profile'), self.user_1.get('id'))
        self.assertEqual(self.user_2_menu_item_1.get('user_profile'), self.user_2.get('id'))
        self.assertEqual(self.user_2_menu_item_2.get('user_profile'), self.user_2.get('id'))

        """ Test that all item orders have been created """
        self.assertTrue(self.user_1_menu_item_1_order_1)
        self.assertTrue(self.user_1_menu_item_1_order_2)
        self.assertTrue(self.user_1_menu_item_2_order_1)
        self.assertTrue(self.user_1_menu_item_2_order_2)
        self.assertTrue(self.user_2_menu_item_1_order_1)
        self.assertTrue(self.user_2_menu_item_1_order_2)
        self.assertTrue(self.user_2_menu_item_2_order_1)
        self.assertTrue(self.user_2_menu_item_2_order_2)

    def test_other_user_and_unauthenticated_user_cannot_get_user_menu_item_order(self):
        """ Test that another user cannot get another user's orders """ 

        user_1_get_user_2_menu_item_1_item_order_1 = self.authorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_1_order_1.get('id')
                }
            ),
            format='json'
        )

        user_1_get_user_2_menu_item_1_item_order_2 = self.authorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_1_order_2.get('id')
                }
            ),
            format='json'
        )

        user_1_get_user_2_menu_item_2_item_order_1 = self.authorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_2.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_2_order_1.get('id')
                }
            ),
            format='json'
        )
        
        user_1_get_user_2_menu_item_2_item_order_2 = self.authorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_2.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_2_order_2.get('id')
                }
            ),
            format='json'
        )

        user_2_get_user_1_menu_item_1_item_order_1 = self.other_authorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_1_order_1.get('id')
                }
            ),
            format='json'
        )

        user_2_get_user_1_menu_item_1_item_order_2 = self.other_authorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_1_order_2.get('id')
                }
            ),
            format='json'
        )

        user_2_get_user_1_menu_item_2_item_order_1 = self.other_authorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_2.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_2_order_1.get('id')
                }
            ),
            format='json'
        )

        user_2_get_user_1_menu_item_2_item_order_2 = self.other_authorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_2.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_2_order_2.get('id')
                }
            ),
            format='json'
        )

        unauthorized_client_get_user_1_menu_item_2_item_order_2 = self.unauthorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_2.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_2_order_2.get('id')
                }
            ),
            format='json'
        )

        unauthorized_client_get_user_2_menu_item_2_item_order_2 = self.unauthorized_client.get(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_2.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_2_order_2.get('id')
                }
            ),
            format='json'
        )

        self.assertEqual(user_1_get_user_2_menu_item_1_item_order_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_1_get_user_2_menu_item_1_item_order_2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_1_get_user_2_menu_item_2_item_order_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_1_get_user_2_menu_item_2_item_order_2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_2_get_user_1_menu_item_1_item_order_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_2_get_user_1_menu_item_1_item_order_2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_2_get_user_1_menu_item_2_item_order_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_2_get_user_1_menu_item_2_item_order_2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(unauthorized_client_get_user_1_menu_item_2_item_order_2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(unauthorized_client_get_user_2_menu_item_2_item_order_2.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_and_unauthenticated_user_cannot_delete_user_menu_item_order(self):
        """ Test that only user that created item order can put item order """

        put_data = {
            'quantity': 69,
            'additional_notes': '6969'
        }

        user_1_put_item_1_order_1 = self.authorized_client.put(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_1_order_1.get('id')
                }
            ),
            put_data,
            format='json'
        )

        user_2_put_user_1_item_1_order_1 = self.other_authorized_client.put(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_1_order_1.get('id')
                }
            ),
            put_data,
            format='json'
        )

        user_1_put_user_2_item_1_order_1 = self.authorized_client.put(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_1_order_1.get('id')
                }
            ),
            put_data,
            format='json'
        )

        unauthorized_client_put_user_2_item_1_order_1 = self.unauthorized_client.put(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_1_order_1.get('id')
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(user_1_put_item_1_order_1.status_code, status.HTTP_200_OK)
        self.assertEqual(user_1_put_item_1_order_1.json().get('id'), self.user_1_menu_item_1_order_1.get('id'))
        self.assertEqual(user_1_put_item_1_order_1.json().get('quantity'), put_data.get('quantity'))
        self.assertEqual(user_1_put_item_1_order_1.json().get('additional_notes'), put_data.get('additional_notes'))
        self.assertEqual(user_2_put_user_1_item_1_order_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_1_put_user_2_item_1_order_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(unauthorized_client_put_user_2_item_1_order_1.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_and_unauthenticated_user_cannot_delete_user_menu_item_order(self):
        """ Test that only user that created item order can delete item order """
        
        user_1_delete_item_1_order_1 = self.authorized_client.delete(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_1_order_1.get('id')
                }
            ),
            format='json'
        )

        user_2_delete_user_1_item_1_order_2 = self.other_authorized_client.delete(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_1.get('full_business_name'),
                    'menu_item_name': self.user_1_menu_item_2.get('url_param_name'),
                    'item_order_pk': self.user_1_menu_item_1_order_2.get('id')
                }
            ),
            format='json'
        )

        user_1_delete_user_2_item_1_order_1 = self.authorized_client.delete(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_1_order_1.get('id')
                }
            ),
            format='json'
        )

        unauthorized_client_delete_user_2_item_1_order_1 = self.unauthorized_client.delete(
            reverse(
                'api:item_order_detail',
                kwargs={
                    'full_business_name': self.user_2.get('full_business_name'),
                    'menu_item_name': self.user_2_menu_item_1.get('url_param_name'),
                    'item_order_pk': self.user_2_menu_item_1_order_1.get('id')
                }
            ),
            format='json'
        )

        self.assertEqual(user_1_delete_item_1_order_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user_2_delete_user_1_item_1_order_2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user_1_delete_user_2_item_1_order_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(unauthorized_client_delete_user_2_item_1_order_1.status_code, status.HTTP_401_UNAUTHORIZED)
