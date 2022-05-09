from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
