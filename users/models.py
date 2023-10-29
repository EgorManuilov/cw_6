from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=11, verbose_name='телефон', null=True, blank=True)
    avatar = models.ImageField(upload_to='users', verbose_name='аватар', null=True, blank=True)

    name_client = models.CharField(max_length=20, verbose_name='Имя клиента')
    first_name_client = models.CharField(max_length=20, verbose_name='Фамилия клиента', null=True, blank=True)

    user_active = models.BooleanField(default=False, verbose_name='Авторизация')
    key_active = models.CharField(max_length=6, default=None, verbose_name='код авторизации', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []