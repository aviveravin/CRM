
from django.db import models 
from django.contrib.auth.models import User
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

User = settings.AUTH_USER_MODEL

class UserManager(BaseUserManager):
    def _create_user(self, email,password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email = email,
                            is_staff = is_staff,
                            is_superuser = is_superuser,
                            **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, False, False, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """My own custom user class"""

    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name=('email address'))
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural =('users')

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


# Create your models here.
class CRM(models.Model):
    ROLE = (
        ('BDA', 'Business Development Executive'),
        ('CS', 'Customer Support'),
        ('IS', 'Inside Sales'),
        ('CW', 'Content Writing'),
        ('DM', 'Digital Marketing'),
    )
    
    role = models.CharField(max_length=5, choices=ROLE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    place = models.CharField(max_length=60)
    phone = models.BigIntegerField()


    