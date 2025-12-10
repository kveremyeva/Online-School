from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course, Lessons, Subscription
from users.models import User


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            name="test_course",
            description="test_description",
            owner=self.user
        )
        self.lesson = Lessons.objects.create(
            name="test_lesson",
            course=self.course,
            owner=self.user,
            video_url="https://www.youtube.com/watch?v=test123"
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест получения урока"""
        url = reverse("course:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тест создания урока"""
        url = reverse("course:lesson-create")
        data = {
            "name": "Новый урок",
            "description": "Описание нового урока",
            "video_url": "https://www.youtube.com/watch?v=new123",
            "course": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lessons.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест обновления урока"""
        url = reverse("course:lesson-update", args=(self.lesson.pk,))
        data = {"name": "Обновленный урок"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Обновленный урок")

    def test_lesson_delete(self):
        """Тест удаления урока"""
        url = reverse("course:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lessons.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест списка уроков"""
        url = reverse("course:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 1)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            name="test_course",
            description="test_description"
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тест создания подписки"""
        url = reverse("course:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(
            user=self.user,
            course=self.course
        ).exists())

    def test_subscription_delete(self):
        """Тест удаления подписки"""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("course:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка удалена")
        self.assertFalse(Subscription.objects.filter(
            user=self.user,
            course=self.course
        ).exists())

    def test_subscription_course_not_found(self):
        """Тест подписки на несуществующий курс"""
        url = reverse("course:subscription")
        data = {"course_id": 999}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscription_no_course_id(self):
        """Тест подписки без course_id"""
        url = reverse("course:subscription")
        data = {}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
