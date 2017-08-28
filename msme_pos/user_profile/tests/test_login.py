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
