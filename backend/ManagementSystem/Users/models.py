from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """
    Custom user model manager where email address is the unique identifier for authentication instead of username.
    """

    def create_user(self, email, first_name, last_name, work_phone,
                    password=None, **extra_fields):
        """
        Create and save a user with given credentials that are mandatory and extra_fields that are supplementary.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, work_phone=work_phone, **extra_fields)

        # might throw a ValidationError
        if password is None:
            password = User.objects.make_random_password(length=14)
        else:
            password_validation.validate_password(password=password)

        user.set_password(password)
        # might throw a ValidationError
        user.clean_fields()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password,  first_name, last_name, work_phone, **extra_fields):
        user = self.create_user(email, first_name, last_name, work_phone, password,  **extra_fields)
        user.is_superuser = True
        user.is_staff = True

       # password_validation.validate_password(password, user)
       # user.set_password(password)

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that takes email as username field. Additionally has some more useful fields.
    """
    email = models.EmailField(_('email address'), unique=True)

    # Validator for names that takes only letters
    letters_validator = RegexValidator(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]*$', 'Only letters are allowed.')

    first_name = models.CharField(max_length=40, validators=[letters_validator,])
    last_name = models.CharField(max_length=40, validators=[letters_validator,])
    work_phone = PhoneNumberField()

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'work_phone']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def generate_uid(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

    def generate_mail_token(self):
        return default_token_generator.make_token(self)

    def send_mail(self, current_site, html_template, subject):
        """Method that sends mail with account activation link."""

        data = {
            'subject': subject,
            'body': render_to_string(html_template, {
                'user': self,
                'domain': current_site.domain,
                'uid': self.generate_uid(),
                'token': self.generate_mail_token(),
            }),
            'recipient': self.email
        }

        print(data['body'])
        #send_mail(data)
