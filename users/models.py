from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель - Пользователь"""
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите вашу почту')
    phone_number = models.CharField(max_length=35, verbose_name='Телефон', help_text='Укажите ваш номер телефона')
    avatar = models.ImageField(upload_to='users/avatar', blank=True, null=True, verbose_name='Аватар',
                               help_text='Загрузите ваш аватар')
    city = models.CharField(max_length=150, verbose_name='Город', help_text='Напишите ваш город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
