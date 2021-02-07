from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .serializers import RegisterSerializer, PasswordSetSerializer, ForgotPasswordSerializer
from .utils import send_mail
from .permissions import VerifiedPermission, SingleUseLinkPermission


User = get_user_model()


@permission_classes([IsAdminUser])
class RegisterView(generics.CreateAPIView):
    """
    Register view, if provided data in a request is validated successfully then
    here it sends a mail with verification link that valid until user sets password
    or after some time defined in settings as PASSWORD_RESET_TIMEOUT variable.

    Only admin user may invoke that view, though he does not set user's password.


    """
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        serializer.create(validated_data)
        user = User.objects.get(email=validated_data.get('email'))

        # It needs to be changed to frontend url
        token = default_token_generator.make_token(user)
        current_site = get_current_site(request)
        data = {
            'subject': 'Activate your account.',
            'body': render_to_string('Users/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            }),
            'recipient': user.email
        }
        print(data['body'])

        #send_mail(data)
        return Response(validated_data, status=status.HTTP_201_CREATED)


@permission_classes([VerifiedPermission])
class ForgotPasswordView(APIView):
    """
    Forgot password view that verifies user existence in db, so as verification status.
    After successful validation, it sends mail with one-time link that allows to configure new password.
    """
    def post(self, request):
        User = get_user_model()
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=serializer.data.get('email'))

            current_site = get_current_site(request)
            token = default_token_generator.make_token(user)
            data = {
                'subject': 'Password reset.',
                'body': render_to_string('Users/reset_password.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                }),
                'recipient': user.email
            }
            user.save()

            #send_mail(data)
            print(data['body'])
            content = {'message': 'Check your inbox, there should be a mail with a link.'
                                  'If you have not received the mail, try checking in spam'}
            return Response(content, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([SingleUseLinkPermission])
class VerifyTempToken(APIView):
    """
    It just verifies whether password reset link is valid.
    if it wasn't for that view, users would have to input new passwords,
    before finding out that the link has already expired or is just broken.
    """
    def get(self, request, uidb64, token):
        return Response({'token': token, 'uidb64' : uidb64}, status=status.HTTP_200_OK)


class ActivateAccount(VerifyTempToken):
    """
    View that activates user account based on link which was sent to the given email address
    It inherits from the VerifyTempToken view because it needs to check if the link hasn't been used before
    or if it isn't broken.
    """
    User = get_user_model()

    def get(self, request, uidb64, token):
        response = super(ActivateAccount, self).get(request, uidb64, token)
        if response.status_code == 200:
            try:
                # Decoding uidb64 in order to get user
                user = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
                if user.is_verified:
                    # return 204 if user has already been verified
                    content = {'message': 'Your account was already verified.'}
                    return Response(content, status=status.HTTP_204_NO_CONTENT)

                # Setting verification flag.
                user.is_verified = True
                user.save()

                return response
            except User.DoesNotExist:
                # probably link was wrong or the user has just been deleted
                return Response({'message': 'Link is probably broken.'}, status=status.HTTP_404_NOT_FOUND)
        return response


@permission_classes([SingleUseLinkPermission])
class PasswordSetView(generics.UpdateAPIView):
    """
    Password set/reset view that updates user's password.
    Only for users that pass one-time link permission verification.
    """
    serializer_class = PasswordSetSerializer
    User = get_user_model()

    def patch(self, request, *args, **kwargs):
        # decoding uid that is sent in request's body
        uid = urlsafe_base64_decode(request.data.get('uidb64')).decode()
        instance = User.objects.get(pk=uid)

        serializer = self.get_serializer(instance, data=request.data)

        # Validation
        serializer.is_valid(raise_exception=True)

        # saving changes to database
        serializer.save(instance, serializer.validated_data)

        content = {'message': 'Password has been updated successfully.'}
        return Response(content, status=status.HTTP_200_OK)


class PasswordChangeView(generics.UpdateAPIView):
    """
    Password change view that enables changing password for authenticated users.
    It requires old password, if old and new password pass validation then
    user's password is updated.
    """
    serializer_class = PasswordSetSerializer
    def patch(self, request, *args, **kwargs):
        instance = request.user

        # validation of data
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instance, serializer.validated_data)

        content = {'message': 'Password has been updated successfully'}
        return Response(content, status=status.HTTP_200_OK)
