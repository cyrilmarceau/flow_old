import logging

from django.contrib.auth import (
    get_user_model,
    authenticate
)
from rest_framework.response import Response
from rest_framework import serializers

from rest_framework.serializers import ModelSerializer
logger = logging.getLogger(__name__)

class UserSerializer(ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'firstname', 'password', 'lastname', 'phone', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
    
        return user


class AuthTokenserializer(serializers.Serializer):
    """Serializer for user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate the authenticated user"""

        logger.debug(' -- attrs -- {}'.format(attrs))

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError('Impossible de s\'authentifier avec ces identifiants')

        # logger.debug('user -- {}'.format(user))
        attrs['user'] = user
        return attrs