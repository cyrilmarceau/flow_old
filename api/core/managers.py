
import logging
from django.contrib.auth.base_user import BaseUserManager

logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    """
    Custom user model manager with email as unique identifier 
    """

    def create_user(self, email, password, **extra):
        """
        Create and save a User with email and password
        """

        if not email:
            raise ValueError('L\'email est obligatoire')


        email = self.normalize_email(email)

        user = self.model(email=email, **extra)
    
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra):
        """
        Create and save Superuser with the given email and password
        """

        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_active', True)

        # if extra.get('is_staff') is not True:
        #     raise ValueError('SuperUser must have is_staff=True')
        # if extra.get('is_superuser') is not True:
        #     raise ValueError('SuperUser must have is_superuser=True')

        return self.create_user(email, password, **extra)