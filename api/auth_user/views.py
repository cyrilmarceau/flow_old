import logging

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import (
    UserSerializer, AuthTokenserializer
)

logger = logging.getLogger(__name__)

class CreateUserView(generics.CreateAPIView):
    """Create new user"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """"Create authen token for user"""

    serializer_class = AuthTokenserializer

    def post(self, request, *args, **kwargs):

        logger.debug('--- {}'.format(request.data))

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        logger.debug(' -- created --', token)

        return Response({
            'token': token.key,
            'user': {
                'id': user.pk,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': user.email,
                'phone': user.phone,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'last_login': user.last_login,
            }
        })



