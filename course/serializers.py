from rest_framework import serializers

from course.models import Course, Lessons


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lessons
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonsSerializer(source='lessons_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons_set.count()
