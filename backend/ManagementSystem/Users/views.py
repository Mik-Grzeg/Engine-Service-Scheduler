from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
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

from .serializers import CustomTokenObtainSerializer, RegisterSerializer
from .utils import send_mail


User = get_user_model()

class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny, )
    serializer_class = CustomTokenObtainSerializer

@permission_classes([IsAdminUser])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permissions_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        self.perform_create(serializer)
        user = User.objects.get(email=validated_data.get('email'))
        print(user)
        # It needs to be changed to frontend url
        current_site = get_current_site(request)
        data= {
            'subject': 'Activate your account.',
            'body': render_to_string('Users/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }),
            'recipient': user.email
        }

        send_mail(data)
        return Response(validated_data, status=status.HTTP_201_CREATED)

@permission_classes([AllowAny])
class ActivateView(APIView):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if user.is_verified:
                content = {'message': 'Your account was already verified.'}
                return Response(content, status=status.HTTP_204_NO_CONTENT)
            user.is_verified = True
            user.save()
            content = {'message': 'Thank you for your verification.\nNow you can log in.'}
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

