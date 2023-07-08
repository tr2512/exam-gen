from rest_framework import serializers

from .models import Course, Quizz, TeacherCourse

class CourseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description', 'long_description')

class QuizzListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quizz
        fields = ('id', 'title', 'slug', 'qtype', 'content', 'created_at')

class TCListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherCourse
        fields = ('id', 'teacher_id', 'course_id')