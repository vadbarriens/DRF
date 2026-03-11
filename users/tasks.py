from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription
from celery import shared_task
from users.models import User
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_course_update_emails(course_id):
    """
    Асинхронная задача для отправки уведомлений об обновлении курса
    """
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user', 'course')

    for subscription in subscriptions:
        subject = f'Обновление курса {subscription.course.title}'
        message = f'Уважаемый {subscription.user.username},\n\nКурс "{subscription.course.title}" был обновлен. Новые материалы доступны для изучения!\n\nС уважением,\nКоманда платформы'

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )


@shared_task
def deactivate_inactive_users():
    """
    Задача для деактивации пользователей, которые не заходили более месяца
    """
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=month_ago,
        is_active=True
    )

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Деактивировано {count} неактивных пользователей"
