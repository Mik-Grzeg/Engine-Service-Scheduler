from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserTestCase(TestCase):
    user = get_user_model()
    password = '$Kasdm123ca'
    email = 'email@mail.com'
    first_name = 'firśt'
    last_name = 'ląst'
    work_phone = '+48123456789'

    def test_create_valid_user(self):
        user = self.user.objects.create_user(email=self.email,
                                             first_name=self.first_name, last_name=self.last_name,
                                             work_phone=self.work_phone)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Checking if there were no mistakes
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.work_phone, self.work_phone)

    def test_model_str(self):
        user = self.user.objects.create_user(email=self.email,
                                             first_name=self.first_name, last_name=self.last_name,
                                             work_phone=self.work_phone)
        self.assertEqual(str(user), 'firśt ląst')

    def test_create_blank_user(self):
        with self.assertRaises(TypeError):
            self.user.objects.create_user()

    def test_create_invalid_email(self):
        with self.assertRaises(ValidationError):
            self.user.objects.create_user(email='',
                                          first_name=self.first_name, last_name=self.last_name,
                                          work_phone=self.work_phone)
            self.user.objects.create_user(email='emailaddress',
                                          first_name=self.first_name, last_name=self.last_name,
                                          work_phone=self.work_phone)
            self.user.objects.create_user(email='email@@mail.com',
                                          first_name=self.first_name, last_name=self.last_name,
                                          work_phone=self.work_phone)
            self.user.objects.create_user(email='email@mail',
                                          first_name=self.first_name, last_name=self.last_name,
                                          work_phone=self.work_phone)

    def test_create_invalid_names(self):
        with self.assertRaises(ValidationError):
            self.user.objects.create_user(email=self.email,
                                          first_name='123name', last_name='ąż@#$123456789123456789123456789123456789123456789',
                                          work_phone=self.work_phone)

    def test_create_valid_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(email=self.email, password=self.password,
                                             first_name=self.first_name, last_name=self.last_name,
                                             work_phone=self.work_phone )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

