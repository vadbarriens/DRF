from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        # Создаем группу модераторов
        from django.contrib.auth.models import Group
        moder_group, _ = Group.objects.get_or_create(name='moders')
        # Создаем пользователей
        self.user = User.objects.create(
            email='test@test.com',
            password='testpass'
        )
        self.moderator = User.objects.create(
            email='moder@test.com',
            password='moderpass',
            is_staff=True
        )
        self.moderator.groups.add(moder_group)  # Добавляем в группу модераторов

        # Создаем курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user,
            amount=100

        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            owner=self.user,
            link_video='https://www.youtube.com/watch?v=test',
            amount=100
        )

        # URL для тестирования
        self.list_url = reverse('materials:lesson_list')
        self.create_url = reverse('materials:lesson_create')
        self.retrieve_url = reverse('materials:lesson_retrieve', kwargs={'pk': self.lesson.pk})
        self.update_url = reverse('materials:lesson_update', kwargs={'pk': self.lesson.pk})
        self.delete_url = reverse('materials:lesson_delete', kwargs={'pk': self.lesson.pk})

    def test_lesson_list_authenticated(self):
        """Тест получения списка уроков авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_lesson_list_unauthenticated(self):
        """Тест получения списка уроков неавторизованным пользователем"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create_owner(self):
        """Тест создания урока владельцем"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.pk,
            'link_video': 'https://youtube.com/watch?v=test',
            'owner': self.user.pk,
            'amount': 100
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_moderator(self):
        """Тест на то, что модератор не может создать урок"""
        self.client.force_authenticate(user=self.moderator)
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.pk,
            'link_video': 'https://youtube.com/valid',
            'owner': self.moderator.pk
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_retrieve_owner(self):
        """Тест получения урока владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_lesson_retrieve_moderator(self):
        """Тест получения урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Title')

    def test_lesson_update_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        data = {'title': 'Updated by Moderator'}
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated by Moderator')

    def test_lesson_delete_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_delete_moderator(self):
        """Тест на то, что модератор не может удалить урок"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(
            email='test@test.com',
            password='testpass'
        )

        # Создаем курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user,
            amount=100
        )

        # URL для подписки
        self.subscription_url = reverse('users:subscriptions')

    def test_subscribe_unsubscribe(self):
        self.client.force_authenticate(user=self.user)

        # Подписываемся
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.pk},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # Отписываемся
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.pk},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscribe_unauthenticated(self):
        """Тест на то, что неавторизованный пользователь не может подписаться"""
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_invalid_course(self):
        """Тест подписки на несуществующий курс"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.subscription_url,
            {'course_id': 999}  # Несуществующий ID
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
