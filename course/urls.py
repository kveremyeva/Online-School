from django.urls import path

from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet, LessonsCreateAPIView, LessonsListAPIView, LessonsRetrieveAPIView, \
    LessonsUpdateAPIView, LessonsDestroyAPIView

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create', LessonsCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonsListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>', LessonsRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>', LessonsUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>', LessonsDestroyAPIView.as_view(), name='lesson-delete'),

] + router.urls