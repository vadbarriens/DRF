from django.db import models
from django.conf import settings


class Course(models.Model):
    """Модель - Курс"""
    title = models.CharField(max_length=150, verbose_name='Название курса', help_text='Укажите название курса')
    preview = models.ImageField(upload_to='materials/preview/course', blank=True, null=True, verbose_name='Превью',
                                help_text='Загрузите превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса',
                                   help_text='Напишите описание курса')
    amount = models.PositiveIntegerField(verbose_name='Цена', help_text='Введите цену курса')
    last_updated = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              help_text='Укажите пользователя')

    class Meta:
        """Метаданные"""
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        """Строковый вывод"""
        return self.title

    def save(self, *args, **kwargs):
        # Проверяем, обновляется ли существующий курс
        if self.pk:
            from users.tasks import send_course_update_emails
            # Запускаем асинхронную задачу
            send_course_update_emails.delay(self.id)
        super().save(*args, **kwargs)


class Lesson(models.Model):
    """Модель - Урок"""
    title = models.CharField(max_length=150, verbose_name='Название урока', help_text='Укажите название урока')
    preview = models.ImageField(upload_to='materials/preview/lesson', blank=True, null=True, verbose_name='Превью',
                                help_text='Загрузите превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока',
                                   help_text='Напишите описание урока')
    link_video = models.URLField(blank=True, null=True, verbose_name='Ссылка', help_text='Прикрепите ссылку на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', help_text='Укажите курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              help_text='Укажите пользователя')
    amount = models.PositiveIntegerField(verbose_name='Цена', help_text='Введите цену курса')

    class Meta:
        """Метаданные"""
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        """Строковый вывод"""
        return self.title
