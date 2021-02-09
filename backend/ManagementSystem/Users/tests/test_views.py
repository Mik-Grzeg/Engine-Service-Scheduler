from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from ..views import UserViewSet

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model

import json


class UserViewSetTest(APITestCase):
    """Simple tests for UserViewSet"""

    def setUp(self) -> None:
        self.User = get_user_model()
        self.factory = APIRequestFactory()
        self.client=APIClient()

        self.valid_regular_user = {
            'email': 'mail@mail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'work_phone': '+48123456789'
        }

        self.invalid_user = {
            'email': 'email@mail.com',
            'first_name': 'First',
            'last_name': 'Last',
        }

        self.valid_regular_user2 = {
            'email': 'mail2@mail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'work_phone': '+48123456789'
        }
        self.admin_passwd = 'Pa$$word123'
        self.admin = self.User.objects.create_superuser(
            email='supermail@mail.com',
            password=self.admin_passwd,
            first_name='First',
            last_name='Last',
            work_phone='+48123456789',
            is_verified=True
        )

    def test_user_create(self):
        """User creation test """
        request = self.factory.post('/auth/user/create/',
                                    json.dumps(self.valid_regular_user),
                                    content_type='application/json')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_user_create(self):
        """Invalid user creation test"""
        request = self.factory.post('auth/user/create/',
                                    json.dumps(self.invalid_user),
                                    content_type='application/json')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_list(self):
        """User list test"""

        # Creating 2 temp users
        user1 = self.User.objects.create_user(**self.valid_regular_user)
        user2 = self.User.objects.create_user(**self.valid_regular_user2)

        request = self.factory.get('auth/user/list/')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'get': 'list',})(request)
        user = self.User.objects.get(email=response.data[2].get('email'))

        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user, user2)
        self.assertFalse(user.is_verified)


    def test_user_set_password(self):
        """Check set_password custom action, so as it's permissions classes"""
        user = self.User.objects.create_user(**self.valid_regular_user)
        user.is_verified = True
        user.save()

        uidb64 = user.generate_uid()
        token = user.generate_mail_token()
        passwd = 'Passw0rd123'

        url = '/auth/user/set_password/'
        payload = {
            "uidb64": uidb64,
            "token": token,
            "password1": passwd,
            "password2": passwd
        }

        # first time using link, should be 200
        response = self.client.patch(url, payload, format='json')

        # second time, permissions check should fail and raise NotAcceptable error
        response2 = self.client.patch(url, payload, format='json')

        # refresh user
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check whether the user's password has changed
        self.assertTrue(user.check_password(passwd))

        self.assertEqual(response2.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_verify_link(self):
        """Testing custom action in UserViewSet, that verifies validity of url."""
        user = self.User.objects.create_user(**self.valid_regular_user)
        passwd = 'Passw0rd123'
        user.set_password(passwd)
        user.save()
        user.refresh_from_db()

        uidb64 = user.generate_uid()
        token = user.generate_mail_token()

        url = f'/auth/user/verify_link/{uidb64}/{token}/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual({'token': token, 'uidb64': uidb64}, response.data)

        # checking if authenticated person may invoke that view
        self.client.login(email=user.email, password=passwd)
        response = self.client.get(url)

        # Token is related to the last_login attribute,
        # hence after logging in, hash changes, so the token is no longer valid.
        self.assertEqual(response.data.get('message'), 'That link is broken or it has already been used.')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
'''
    def test_registering_activating_and_setting_password(self):
        """Testing activation account by emailed link, and setting password"""
        login_url = '/auth/login/'
        login_response = self.client.post(login_url, {"email": self.admin.email, "password": self.admin_passwd},
                                          format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(login_response.data), ['refresh', 'access'])

        refresh, access = login_response.data.values()

        # registering new user
        # add token to request header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        register_url = '/auth/user/'
        register_response = self.client.post(register_url,
                                            data=self.valid_regular_user,
                                            format='json'
                                           )
        print(self.User.objects.all())
        user = self.User.objects.get(email=register_response.data.get('email'))
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(register_response.data, self.valid_regular_user)
        self.assertFalse(user.is_verified)

        # creating uidb64 and token, because normally it's sent in mail content.
        uidb64 = user.generate_uid()
        token = user.generate_mail_token()

        # request to activate user's account.
        # remove access token from request header
        self.client.credentials()
        activate_url = f'/auth/user/activate_account/{uidb64}/{token}/'
        activate_response = self.client.get(activate_url)
        user.refresh_from_db()

        self.assertEqual(activate_response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(activate_response.data, {'uidb64': uidb64, 'token': token})
        self.assertTrue(user.is_verified)

        new_password = 'Pa$$w0rd123'
        self.assertFalse(user.check_password(new_password))

        # request to set user's password
        set_password_url = '/auth/user/set_password/'
        set_password_response = self.client.patch(set_password_url,
                                                  data={**activate_response.data,
                                                        'password1': new_password,
                                                        'password2': new_password},
                                                  format='json'
                                                  )
        self.assertEqual(set_password_response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(set_password_response.data, {'message': 'Password has been updated successfully.'})
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))
'''

    def test_forgot_password_unverified_user(self):
        user = self.User.objects.create_user(**self.valid_regular_user)

        url = reverse('user-forgot-password')
        self.client.credentials()
        response = self.client.put(path=url,
                                data={"email": user.email},
                                format='json')

        # Testing user that hasn't been verified yet.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_forgot_password_verified_user(self):
        url = reverse('user-forgot-password')
        self.client.credentials()
        response = self.client.put(path=url,
                              data={"email": self.admin.email},
                              format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), "Check your inbox, there should be a mail with a link."
                                                "If you have not received the mail, try checking in spam")


    def test_change_password(self):
        url = '/auth/user/change_password/'
        old_passwd = 'Pasw0rd123'
        new_passwd = 'Pa$$w0rd123'
        user = self.User.objects.create_user(**self.valid_regular_user, password=old_passwd, is_verified=True)

        # force_authentication because change_password action only needs user to be authenticated and verified
        # which has already been tested
        self.client.force_authenticate(user=user)
        response = self.client.patch(url,
                                     data={'current_password': old_passwd,
                                           'password1': new_passwd,
                                           'password2': new_passwd},
                                     format='json')

        self.assertTrue(user.check_password(new_passwd))
        self.assertDictEqual(response.data, {'message': 'Password has been updated successfully'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)