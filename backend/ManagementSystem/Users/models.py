from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import password_validation

from django.core.validators import RegexValidator

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """
    Custom user model manager where email address is the unique identifier for authentication instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with given credentials that are mandatory and extra_fields that are supplementary.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # might throw a ValidationError
        password_validation.validate_password(password, user)
        user.set_password(password)

        # might throw a ValidationError
        user.clean_fields()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password,  **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
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
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'work_phone']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def is_staff(self):
        return self.is_superuser
