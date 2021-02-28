from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.exceptions import (APIException, MethodNotAllowed,
                                       NotAcceptable, NotAuthenticated,
                                       NotFound)
from rest_framework.permissions import BasePermission, DjangoModelPermissions

User = get_user_model()


class DjangoModelPermissionsWithRead(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class SingleUseLinkPermission(BasePermission):
    """
    Permission class that if the one-time link is valid, which was sent in mail.
    """

    def has_permission(self, request, view):
        """
        Url is composed from:
            uidb64 - encoded pk of the user
            token - generated token, but that token does not allow authentication.
                Moreover, after changing attributes that are part of
                the token, it's no longer valid.
        """
        # uidb64 and token might be passed as kwargs or as request data
        uidb64, token = view.kwargs.get('uidb64'), view.kwargs.get('token')
        if (uidb64 and token) is None:
            uidb64 = request.data.get('uidb64')
            token = request.data.get('token')
        try:
            # If the exception is raised then user could have just been deleted
            # or the uidb64 is wrong.
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except AttributeError:
            raise MethodNotAllowed(method='Password reset', detail={'error': True, 'message': 'You can\'t do that'})
        if user is not None and default_token_generator.check_token(user, token):
            return True
        raise NotAcceptable({'error': True, 'message': 'That link is broken or it has already been used.'})


class VerifiedPermission(BasePermission):
    """
    Permission that checks if user / email has already  been verified by email link.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            # User might be anonymous because it also checks permissions for views like forgot password.
            email = request.data.get('email')
            try:
                user = User.objects.get(email=email)
                verified = user.is_verified
            except User.DoesNotExist:
                # User with the provived email coudln't be found in database.
                detail = {'error': True, 'message': 'We couldn\'t find a user connected to that email address.'}
                raise NotFound(detail)
        else:
            verified = request.user.is_verified

        if verified:
            return True
        raise NeedVerification()


class NeedVerification(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'error': True, 'message': 'Your account hasn\'t been activated yet.'}
    default_code = 'not_verified'
