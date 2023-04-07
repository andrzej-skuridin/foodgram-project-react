from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'user'),
        ('admin', 'admin'),
        ('moderator', 'moderator'),
    ]

    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default='user')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

