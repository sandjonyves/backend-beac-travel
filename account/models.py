from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import datetime

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse e-mail doit être spécifiée.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=32, null=True)
    firstName = models.CharField(max_length=32,null=True)
    latsName = models.CharField(max_length=32,null=True)
    username = models.CharField(max_length=32,null=True)
    admin_id = models.IntegerField(null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    refresh_token = models.TextField(max_length=500,null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['username']

    class Role(models.TextChoices):
        AGENT = "AGENT", "agent"
        ADMIN = "ADMIN", "admin"
        SUPERUSER = 'SUPERUSER', "superuser"

    role = models.CharField(max_length=32, choices=Role.choices, default="")

class Agent(CustomUser):
    agency = models.ForeignKey('app.Agency', on_delete=models.CASCADE, related_name='agents',null=True)

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.role = CustomUser.Role.AGENT
        super().save(*args, **kwargs)

class Admin(CustomUser):
    agency = models.OneToOneField('app.Agency', on_delete=models.CASCADE, related_name='admin_user',null=True)

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.role = CustomUser.Role.ADMIN
        super().save(*args, **kwargs)

class Superuser(CustomUser):
    service = models.OneToOneField('app.service',on_delete=models.CASCADE,related_name='superuser',default=1,null=True)
    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.role = CustomUser.Role.SUPERUSER
        super().save(*args, **kwargs)

class RevokedToken(models.Model):
    token = models.CharField(max_length=512, unique=True)  
    revoked_at = models.DateTimeField(default=datetime.now) 

    def __str__(self):
        return self.token