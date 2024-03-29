from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from .permissions import SingleUseLinkPermission, VerifiedPermission

User = get_user_model()


class GroupView(ModelViewSet):
    """Group viewset"""

    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.all()


class LoginView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns first name of the user, an access and refresh JSON web
    token pair to prove authentication of those credentials.
    """
    serializer_class = serializers.LoginSerializer


class UserViewSet(ModelViewSet):
    """
    User View Set
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        """Getting proper serializers for specific actions."""
        if self.action == 'change_password':
            return serializers.PasswordChangeSerializer
        if self.action == 'set_password':
            return serializers.PasswordSetSerializer
        if self.action == 'forgot_password':
            return serializers.ForgotPasswordSerializer
        return serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Method for creating new users, it sends a mail with verification link that is valid,
        until user sets password or after some time defined in settings as PASSWORD_RESET_TIMEOUT variable.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # Setting variables that are content of an email
        current_site = get_current_site(request)
        html_template = 'Users/account_activation.html'
        subject = 'Account activation.'

        # sending verification link to the provided email address
        user.send_mail(current_site, html_template, subject)
        # If no exception has been raised, 201 is returned.

        return Response(serializer.initial_data,
                        status=status.HTTP_201_CREATED,
                        headers=self.get_success_headers(serializer.initial_data))

    def perform_create(self, serializer):
        return serializer.create()

    @action(detail=False, methods=['patch'], permission_classes=[SingleUseLinkPermission])
    def set_password(self, request):
        """
        Method that allows to set / reset password if user has just been created
        or user has forgotten it.
        """

        # Decoding uid that is provided in request
        uid = urlsafe_base64_decode(request.data.get('uidb64')).decode()
        instance = User.objects.get(pk=uid)
        serializer = self.get_serializer(data=request.data, instance=instance)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        content = {'message': _('Password has been updated successfully.')}
        return Response(content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[SingleUseLinkPermission & ~IsAuthenticated],
            url_path=r'verify_link/(?P<uidb64>.+)/(?P<token>.+)', url_name='verify-link')
    def verify_one_time_link(self, request, uidb64, token):
        """
        It just verifies whether password reset link is valid.
        if it wasn't for that view, users would have to input new passwords,
        before finding out that the link has already expired or is just broken.
        """
        return Response({'token': token, 'uidb64': uidb64}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[SingleUseLinkPermission & ~IsAuthenticated],
            url_path=r'activate_account/(?P<uidb64>.+)/(?P<token>.+)')
    def activate_account(self, request, uidb64, token):
        """
        Method that activates user account based on link, which was sent to the given email address.
        permission_classes SingleUseLinkPermission checks if the link is valid.
        """
        # Decoding uidb64 in order to get user
        user = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
        if user.is_verified:
            # return 204 if user has already been verified
            content = {'message': _('Your account was already verified.')}
            return Response(content, status=status.HTTP_204_NO_CONTENT)

        # Setting verification flag.
        user.is_verified = True
        user.save()

        return Response({'token': token, 'uidb64': uidb64}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], permission_classes=[VerifiedPermission & ~IsAuthenticated])
    def forgot_password(self, request):
        """
        Forgot password method that verifies user existence in db, so as verification status.
        After successful validation, it sends mail with one-time link that allows to configure new password.
        """

        # Setting variables that are content of an email
        html_template = 'Users/reset_password.html'
        current_site = get_current_site(request)
        subject = 'Password reset.'

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Getting user in order to invoke send_mail method.
            user = User.objects.get(email=serializer.validated_data.get('email'))
            user.send_mail(current_site, html_template, subject)

            content = {'message': _('Check your inbox, there should be a mail with a link.'
                                    'If you have not received the mail, try checking in spam')}
            return Response(content, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'], permission_classes=[VerifiedPermission & IsAuthenticated])
    def change_password(self, request):
        """
        Method that allows user to change this password,
        though he has to be logged in and remember his old password.
        """
        # instance = request.user
        # validation of data
        # serializer = serializers.PasswordChangeSerializer(data=request.data, instance=instance)
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        content = {'message': _('Password has been updated successfully')}
        return Response(content, status=status.HTTP_200_OK)
