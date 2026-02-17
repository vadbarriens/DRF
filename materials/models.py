from django.db import models


class Course(models.Model):
    """Модель - Курс"""
    title = models.CharField(max_length=150, verbose_name='Название курса', help_text='Укажите название курса')
    preview = models.ImageField(upload_to='materials/preview/course', blank=True, null=True, verbose_name='Превью',
                                help_text='Загрузите превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса',
                                   help_text='Напишите описание курса')

    class Meta:
        """Метаданные"""
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        """Строковый вывод"""
        return self.title


class Lesson(models.Model):
    """Модель - Урок"""
    title = models.CharField(max_length=150, verbose_name='Название урока', help_text='Укажите название урока')
    preview = models.ImageField(upload_to='materials/preview/lesson', blank=True, null=True, verbose_name='Превью',
                                help_text='Загрузите превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока',
                                   help_text='Напишите описание урока')
    link_video = models.URLField(blank=True, null=True, verbose_name='Ссылка', help_text='Прикрепите ссылку на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', help_text='Укажите курс')

    class Meta:
        """Метаданные"""
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        """Строковый вывод"""
        return self.title
