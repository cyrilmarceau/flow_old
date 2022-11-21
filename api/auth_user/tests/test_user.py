
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import User

from rest_framework import status
from rest_framework.test import APIClient

TEST_CREATE_USER_URL = reverse('user:create') # Termination endpoint
TEST_TOKEN_URL = reverse('user:token')

PAYLOAD_USER = {
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

        res = self.client.post(TEST_CREATE_USER_URL, PAYLOAD_USER)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        User = get_user_model()

        user = User.objects.get(email=PAYLOAD_USER.get('email'))

        self.assertTrue(user.check_password(PAYLOAD_USER.get('password')))

        # Check if password is not set in a response
        self.assertNotIn('password', res.data) 

    def test_user_with_email_exists_error(self):
        """Test error if user with email exist"""

        # Same payload for precedent test so email exist
        create_user(**PAYLOAD_USER)

        res = self.client.post(TEST_CREATE_USER_URL, PAYLOAD_USER)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short(self):
        """Test error if password < 5 char"""

        PAYLOAD_USER.update({'password': 'test'})
        
        res = self.client.post(TEST_CREATE_USER_URL, PAYLOAD_USER)
        
        # Status need to be return
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 

        User = get_user_model()
        user_exist = User.objects.filter(email=PAYLOAD_USER.get('email')).exists()
        
        # Check user is not create
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """"Test create token for valid credentials"""

        USER = {
            'email': 'john@example.com',
            'firstname': 'John',
            'lastname': 'Doe',
            'phone': '0102030405',
            'password': 'testTest'
        }

        create_user(**USER)

        PAYLOAD = {
            'email': PAYLOAD_USER.get('email'),
            'password': PAYLOAD_USER.get('password')
        }

        res = self.client.post(TEST_TOKEN_URL, PAYLOAD)

        self.assertIn('token', res.token)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error if credential was invalid"""

        USER = {
            'email': 'john@example.com',
            'firstname': 'John',
            'lastname': 'Doe',
            'phone': '0102030405',
            'password': 'testTest'
        }

        create_user(**USER)

        payload = {'email': 'johnn@example.com', 'password': 'invalidPassword'}

        res = self.client.post(TEST_TOKEN_URL, payload)

        res.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """"Test return error if token was not set"""

        payload = {'email': 'john@example.com', 'password': ''}

        res = self.client.post(TEST_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertFalse('password')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


