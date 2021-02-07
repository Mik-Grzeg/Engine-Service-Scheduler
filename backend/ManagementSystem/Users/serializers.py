from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
       )
    work_phone = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'work_phone')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            work_phone=validated_data['work_phone'],
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


    def __init__(self, *args, **kwargs):
        """
        If there was current_password passed then add new field to the serializer.
        """
        super(PasswordSetSerializer, self).__init__(*args, **kwargs)
        current_password = self.context['request'].data.get('current_password')
        if current_password:
            self.fields['current_password'] = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        """
        Checks if current_password is correct.
        """
        if not self.instance.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

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

    def save(self, instance, validated_data):
        print(validate_password(validated_data['password1'], instance))
        instance.set_password(validated_data['password1'])

        instance.save()
        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)