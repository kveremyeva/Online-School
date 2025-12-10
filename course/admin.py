from django.contrib import admin

from course.models import Course, Lessons, Subscription
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'city')
    search_fields = ('email', 'phone', 'city')
    ordering = ('email',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Lessons)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'video_url')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'subscribed_at')
    list_filter = ('course', 'subscribed_at')
