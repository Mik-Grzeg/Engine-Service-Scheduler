from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class GroupListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Default result (access/refresh tokens)
        data = super(LoginSerializer, self).validate(attrs)

        # Adding custom data
        data.update({'first_name': self.user.first_name})

        return data


class UserSerializer(ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
       )
    work_phone = serializers.CharField(required=True)
    groups = serializers.SlugRelatedField(queryset=Group.objects.all(), slug_field='name', many=True, required=False)
    user_permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'work_phone', 'groups', 'user_permissions')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def get_user_permissions(self, obj):
        """Method that returns all permissions of the user"""
        if isinstance(obj, User):
            if obj.is_superuser:
                permissions = Permission.objects.all()
            else:
                permissions = Permission.objects.filter(group__user=obj) |\
                              obj.user_permissions.all()
        else:
            # If the user has just been created then, obj is ordereddict rather than User instance.
            # Hence permissions must be filtered by the names of groups that the user has been assigned to.
            permissions = Permission.objects.filter(group__name__in=obj['groups'])
        return [permission.codename for permission in permissions]



    def create(self):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            work_phone=self.validated_data['work_phone'],
        )

        try:
            groups = self.validated_data['groups']
            for group in groups:
                print(group)
                user.groups.add(group)
        except:
            pass

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