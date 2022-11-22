
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import User

from rest_framework import status
from rest_framework.test import APIClient

TEST_CREATE_USER_URL = reverse('user:create') # Termination endpoint
TEST_TOKEN_URL = reverse('user:token')
TEST_ME = reverse('user:me')

USER_DETAILS = {
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

        res = self.client.post(TEST_CREATE_USER_URL, USER_DETAILS)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        User = get_user_model()

        user = User.objects.get(email=USER_DETAILS.get('email'))

        self.assertTrue(user.check_password(USER_DETAILS.get('password')))

        # Check if password is not set in a response
        self.assertNotIn('password', res.data) 

    def test_user_with_email_exists_error(self):
        """Test error if user with email exist"""

        # Same payload for precedent test so email exist
        create_user(**USER_DETAILS)

        res = self.client.post(TEST_CREATE_USER_URL, USER_DETAILS)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short(self):
        """Test error if password < 5 char"""

        USER_DETAILS.update({'password': 'test'})
        
        res = self.client.post(TEST_CREATE_USER_URL, USER_DETAILS)
        
        # Status need to be return
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 

        User = get_user_model()
        user_exist = User.objects.filter(email=USER_DETAILS.get('email')).exists()
        
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
            'email': USER_DETAILS.get('email'),
            'password': USER_DETAILS.get('password')
        }

        res = self.client.post(TEST_TOKEN_URL, PAYLOAD)

        self.assertIn('token', res.data)
        self.assertIn('user', res.data)

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

        payload = {'email': 'john@example.com', 'password': 'invalidPassword'}

        res = self.client.post(TEST_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """"Test return error if token was not set"""

        payload = {'email': 'john@example.com', 'password': ''}

        res = self.client.post(TEST_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_user_nautorize(self):
        """Test autorization required for user"""

        res = self.client.get(TEST_ME)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserAPI(TestCase):
    """Test API request for authenticated user"""

    def setUp(self):

        self.user_detail = {
            "id": 4,
            "firstname": "cyril",
            "lastname": "marceau",
            "email": "ecmarceau@emend1o.fr",
            "phone": "0102030405",
            "password": "testTest",
            "created_at": "2022-11-21T20:45:31.328623Z",
            "updated_at": "2022-11-21T20:45:31.328664Z",
            "last_login": None
        }

        self.user = create_user(**self.user_detail)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_profil_success(self):
        """Test retrieving profil for user logged"""

        res = self.client.get(TEST_ME)

        self.assertEqual(res.data, {
            'id': self.user.id,
            'firstname': self.user.firstname,
            'lastname': self.user.lastname,
            'email': self.user.email,
            'phone': self.user.phone,
            'created_at': self.user.created_at,
            'updated_at': self.user.updated_at,
            'last_login': self.user.last_login,
        })
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)

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

        self.assertEqual(self.user, {
            'id': self.user_detail.get('id'),
            'firstname': payload_update.get('firstname'),
            'lastname': self.user_detail.get('lastname'),
            'email': self.user_detail.get('email'),
            'phone': self.user_detail.get('phone'),
            'created_at': self.user_detail.get('created_at'),
            # 'updated_at': self.user_detail.get('updated_at'),
            'last_login': self.user_detail.get('last_login'),
        })

        self.assertTrue(self.user.check_password(self.user_detail.get('password')))

        self.assertEqual(res.status_code, status.HTTP_200_OK)