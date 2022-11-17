from django.test import TestCase
from django.contrib.auth import get_user_model

class UsersTests(TestCase):

    def test_create_user(self):
        """Test creating user successful"""

        email = 'john@example.com'
        password = 'password123'

        User = get_user_model()

        extra = {"firstname": "John", "lastname": "Doe", "phone": "0102030405"}

        user = User.objects.create_user(
            email=email,
            password=password,
            **extra
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_user_email_normalized(self):
        """Test if email is normalized for new user"""
        
        emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com']
        ]

        

        for email, expected in emails:
            User = get_user_model()

            user = User.objects.create_user(email, 'passwordTest')

            self.assertEqual(user.email, expected)
    
    def test_create_user_without_email(self):
        """Test create user without email raise Value error"""

        with self.assertRaises(ValueError):
            User = get_user_model()
            User.objects.create_user('', 'passwordTest')

    def test_create_superuser(self):
        """Create an super user"""
        
        User = get_user_model()
        user = User.objects.create_superuser(
            "test@example.com",
            'testPassword'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)