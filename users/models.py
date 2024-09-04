from django.db import models
from django.utils import timezone
import string
import random
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Gender(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,  null=True, blank=True)
    age = models.IntegerField( null=True, blank=True)
    email = models.EmailField(unique=True)
    number = models.IntegerField( null=True, blank=True)
    wholesaler = models.BooleanField(default=False,  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #for wholesaler
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_otp():
        digits = string.digits
        return ''.join(random.choice(digits) for i in range(4))

    @property
    def is_expired(self):
        time_threshold = timezone.now() - timezone.timedelta(minutes=5)
        return self.created_at < time_threshold