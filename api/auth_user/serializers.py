from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    """Serializer for user object"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'firstname', 'password', 'lastname', 'phone', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
    
        return user