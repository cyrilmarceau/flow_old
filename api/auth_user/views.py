from rest_framework import generics
from .serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Create new user"""
    serializer_class = UserSerializer