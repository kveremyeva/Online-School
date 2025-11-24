from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course, Lessons, Subscription
from course.paginators import CourseLessonPaginator
from course.permissions import IsModer, IsOwner, CanDeleteLesson
from course.serializers import CourseSerializer, LessonsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ Viewset для курсов"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseLessonPaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, ~IsModer, IsOwner]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Course.objects.none()
        if self.request.user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class LessonsCreateAPIView(generics.CreateAPIView):
    """ Создание уроков"""
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonsListAPIView(generics.ListAPIView):
    """ Список уроков"""
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPaginator

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Lessons.objects.none()
        if self.request.user.groups.filter(name="moderators").exists():
            return Lessons.objects.all()
        return Lessons.objects.filter(owner=self.request.user)


class LessonsRetrieveAPIView(generics.RetrieveAPIView):
    """ Извлечение уроков"""
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonsUpdateAPIView(generics.UpdateAPIView):
    """ Обновление уроков"""
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonsDestroyAPIView(generics.DestroyAPIView):
    """ Удаление уроков"""
    queryset = Lessons.objects.all()
    permission_classes = [CanDeleteLesson]



class SubscriptionAPIView(APIView):
    """Контроллер управления подписками на курсы"""
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        if course_id is None:
            return Response(
                {"error": "course_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course_item = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Курс с указанным ID не существует"},
                status=status.HTTP_404_NOT_FOUND
            )

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})
