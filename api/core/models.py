from typing import List
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Adresse email', max_length=255, unique=True)
    firstname = models.CharField("Prénom", max_length=255, null=True, blank=True)
    lastname = models.CharField("Nom", max_length=255, null=True, blank=True)
    phone = models.CharField(verbose_name="Numéro de téléphone", max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email' # Define the unique identifier
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email