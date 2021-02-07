from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..views import RegisterView

from django.contrib.auth import get_user_model

import json


class RegisterNewUser(TestCase):
    """ Test module for registering new user"""
    def setUp(self) -> None:
        self.User = get_user_model()

        self.valid_payload = {
            'email': 'mail@mail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'work_phone': '+48123456789'
        }

        self.invalid_payload = {
            'email': 'email@mail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password': 'password'
        }

        self.user = self.User.objects.create_superuser(
            email='admin@mail.com',
            password='Pa$$word123',
            first_name='admin',
            last_name='super',
            work_phone='+48123456789'
        )

    def test_register_valid_user(self):
        factory = APIRequestFactory()
        admin = self.user
        view = RegisterView.as_view()

        request = factory.post(
            '/auth/register/',
            json.dumps(self.valid_payload),
            content_type='application/json'
        )
        force_authenticate(request, user=admin)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_invalid_user(self):
        factory = APIRequestFactory()
        admin = self.user
        view = RegisterView.as_view()

        request = factory.post(
            '/auth/register/',
            json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        force_authenticate(request, user=admin)
        response = view(request)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)