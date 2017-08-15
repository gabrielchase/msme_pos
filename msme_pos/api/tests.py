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

    def test_api_can_get_own_user_profile_menu(self):
        menu_item_data_1 = {
            'name': 'menu item 1',
            'description': 'menu item description 1',
            'price': 80
        }

        menu_item_data_2 = {
            'name': 'menu item 2',
            'description': 'menu item description 2',
            'price': 80
        }

        self.client.post(
            reverse('api:menu_items_create'),
            menu_item_data_1,
            format='json'
        )

        self.client.post(
            reverse('api:menu_items_create'),
            menu_item_data_2,
            format='json'
        )

        user_profile_menu = self.client.get(
            reverse(
                'api:profile-menu',
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            format='json'
        )

        self.assertEqual(user_profile_menu.status_code, status.HTTP_200_OK)

        for item in user_profile_menu.json():
            self.assertTrue(item.get('id'))
            self.assertIn(item.get('name'), [menu_item_data_1.get('name'), menu_item_data_2.get('name')])
            self.assertIn(item.get('description'), [menu_item_data_1.get('description'), menu_item_data_2.get('description')])
            self.assertIn(item.get('price'), [format(menu_item_data_1.get('price'), '.2f'), format(menu_item_data_2.get('price'), '.2f')])
            self.assertTrue(item.get('user_profile', {}).get('id'))
            self.assertEqual(item.get('user_profile', {}).get('email'), self.user_data.get('email'))

    def test_api_cannot_get_other_user_profile_menu(self):
        menu_item_data_1 = {
            'name': 'menu item 1',
            'description': 'menu item description 1',
            'price': 80
        }

        self.client.post(
            reverse('api:menu_items_create'),
            menu_item_data_1,
            format='json'
        )

        other_user_client = APIClient()

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

        other_user = other_user_client.post(
            reverse('api:profile-list'),
            other_user_data,
            format='json'
        )

        other_user_login_data = {
            'username': other_user_data.get('email'),
            'password': other_user_data.get('password'),
        }

        other_user_login_response = self.client.post(
            reverse('api:login-list'),
            other_user_login_data,
            format='json'
        )

        other_user_login_token = other_user_login_response.json().get('token')
        other_user_client.credentials(HTTP_AUTHORIZATION='Token ' + other_user_login_token)

        created_user_menu = other_user_client.get(
            reverse(
                'api:profile-menu',
                kwargs={'full_business_name': self.created_user.get('full_business_name')}
            ),
            format='json'
        )

        self.assertEqual(created_user_menu.status_code, status.HTTP_401_UNAUTHORIZED)


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

        print(created_menu_item_response.status_code)
        print(created_menu_item_response.json())

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
            reverse('api:profile-list'),
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

        print(authenticated_user_api_response.status_code)
        print(authenticated_user_api_response.json())

        unauthenticated_client = APIClient()

        unauthenticated_client_response = unauthenticated_client.get(
            reverse('api:menu_items_list'),
            format='json'
        ).json()

        print(unauthenticated_client.status_code)
        print(unauthenticated_client.json())

        superuser_get_menu_list_response = self.superuser_client.get(
            reverse('api:menu_item_list'),
            format='json'
        ).json()

        self.assertEqual(authenticated_user_api_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(unauthenticated_client_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(superuser_get_menu_list_response.status_code, status.HTTP_200_OK)

