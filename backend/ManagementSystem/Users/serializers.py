from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class GroupSerializer(ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='codename'
    )
    user_set = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Group
        fields = ('name', 'permissions', 'user_set')


class UserSerializer(ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
       )
    work_phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'work_phone')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


    def create(self):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            work_phone=self.validated_data['work_phone'],
        )

        return user


class PasswordSetSerializer(serializers.Serializer):
    """
    Serializer that set / change password, depending on context.
    If there is current_password passwd then, the serializer is called because the user has forgot password
    or he has just registered and it's the first time he signs in.
    """
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)


    def validate(self, attrs):
        """
        Check if the two given passwords are the same
        and also whether new password isn't the same as the old one.
        """

        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('New passwords do not match')
        if self.instance.check_password(attrs['password1']):
            raise serializers.ValidationError('New password can not be the same as the old one.')
        return attrs

    def save(self):
        """Setting new password after validation"""
        self.instance.set_password(self.validated_data['password1'])
        self.instance.save()

        return self.instance

class PasswordChangeSerializer(PasswordSetSerializer):
    """
    Password change serializer that inherits from PasswordSet,
    because the only difference is field with old password and its validation.
    """
    current_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        """
        Checks if current_password is correct.
        """
        self.instance.check_password(value)
        return value

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).count() == 0:
            raise serializers.ValidationError('We could not find any user with provided email address.')
        return value