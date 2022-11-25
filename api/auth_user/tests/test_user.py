
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import User
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from rest_framework import serializers

TEST_CREATE_USER_URL = reverse('user:create') # Termination endpoint
TEST_TOKEN_URL = reverse('user:token')
TEST_ME = reverse('user:me')

user_detail = {
    'email': 'john@example.com',
    'firstname': 'John',
    'lastname': 'Doe',
    'phone': '0102030405',
    'password': 'testTest'
}

def create_user(**params):
    """" Create and return an user"""
    User = get_user_model()

    user = User.objects.create_user(**params)
    return user

class PublicUserAPI(TestCase):
    """Test the public feature of user"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""

        user_detail = {
            'email': 'john@example.com',
            'firstname': 'John',
            'lastname': 'Doe',
            'phone': '0102030405',
            'password': 'testTest'
        }

        res = self.client.post(TEST_CREATE_USER_URL, user_detail)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        User = get_user_model()

        user = User.objects.get(email=user_detail.get('email'))

        self.assertTrue(user.check_password(user_detail.get('password')))

        # Check if password is not set in a response
        self.assertNotIn('password', res.data) 

    def test_user_with_email_exists_error(self):
        """Test error if user with email exist"""
        
        user_detail = {
            'email': 'john@example.com',
            'firstname': 'John',
            'lastname': 'Doe',
            'phone': '0102030405',
            'password': 'testTest'
        }

        create_user(**user_detail)

        res = self.client.post(TEST_CREATE_USER_URL, user_detail)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short(self):
        """Test error if password < 5 char"""

        user_detail = {
            'email': 'john1@example.com',
            'firstname': 'John1',
            'lastname': 'Doe1',
            'phone': '0102030405',
            'password': 'test'
        }
        
        res = self.client.post(TEST_CREATE_USER_URL, user_detail)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 

        User = get_user_model()
        user_exist = User.objects.filter(email=user_detail.get('email')).exists()
        
        # Check user is not create
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """"Test create token for valid credentials"""

        user_detail = {
            'email': 'john2@example.com',
            'firstname': 'John2',
            'lastname': 'Doe2',
            'phone': '0102030405',
            'password': 'testTest2'
        }

        create_user(**user_detail)

        payload = {
            'email': user_detail.get('email'),
            'password': user_detail.get('password')
        }

        res = self.client.post(TEST_TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertIn('user', res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error if credential was invalid"""

        user_detail = {
            'email': 'john3@example.com',
            'firstname': 'John3',
            'lastname': 'Doe3',
            'phone': '0102030405',
            'password': 'testTest3'
        }

        create_user(**user_detail)

        payload = {'email': 'john3@example.com', 'password': 'invalidPassword'}

        res = self.client.post(TEST_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """"Test return error if token was not set"""

        payload = {'email': 'john4@example.com', 'password': ''}

        res = self.client.post(TEST_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unautorize(self):
        """Test autorization required for user"""

        res = self.client.get(TEST_ME)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserAPI(TestCase):
    """Test API request for authenticated user"""

    def setUp(self):


        self.user = create_user(
            id=1,
            email='john4@example.com',
            firstname='John4',
            lastname='Doe4',
            phone='0102030405',
            password='testTest4',
            created_at=timezone.now(),
            updated_at=timezone.now(),
            last_login=timezone.now(),
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_profil_success(self):
        """Test retrieving profil for user logged"""

        res = self.client.get(TEST_ME)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, {
            'id': self.user.id,
            'email': self.user.email,
            'firstname': self.user.firstname,
            'lastname': self.user.lastname,
            'phone': self.user.phone,
            'created_at': serializers.DateTimeField().to_representation(self.user.created_at),
            'updated_at': serializers.DateTimeField().to_representation(self.user.updated_at),
            'last_login': serializers.DateTimeField().to_representation(self.user.last_login)
        })
        

    def test_post_me_not_allowed(self):
        """Test POST method is not allowed for me endpoint"""

        res = self.client.post(TEST_ME, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profil(self):
        """Test updating the user profil for authenticated user"""
    
        payload_update = {'firstname': 'John', 'password': 'newPassword'}

        res = self.client.patch(TEST_ME, payload_update)

        # Need to refresh manually
        self.user.refresh_from_db()

        self.assertEqual(res.data, {
            'id': self.user.id,
            'firstname': payload_update.get('firstname'),
            'lastname': self.user.lastname,
            'email': self.user.email,
            'phone': self.user.phone,
            'created_at': serializers.DateTimeField().to_representation(self.user.created_at),
            'updated_at': serializers.DateTimeField().to_representation(self.user.updated_at),
            'last_login': serializers.DateTimeField().to_representation(self.user.last_login)
        })

        self.assertTrue(self.user.check_password(payload_update.get('password')))

        self.assertEqual(res.status_code, status.HTTP_200_OK)