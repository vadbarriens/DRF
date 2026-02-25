from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """Модель - Пользователь"""
    username = None
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


class Payment(models.Model):
    """Модель - Платеж"""
    METHOD_CHOISES = [
        ('Наличные', 'Наличные'),
        ('Перевод', 'Перевод')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Укажите пользователя')
    payment_date = models.DateField(verbose_name='Дата оплаты', help_text='Укажите дату оплаты')
    payment_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс',
                                       help_text='Выберите курс для оплаты')
    payment_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок',
                                       help_text='Выберите урок для оплаты')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты', help_text='Укажите сумму оплаты')
    method = models.CharField(max_length=50, choices=METHOD_CHOISES, verbose_name='Способ оплаты',
                              help_text='Выберите способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
