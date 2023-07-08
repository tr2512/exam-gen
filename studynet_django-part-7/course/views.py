from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CourseListSerializer, QuizzListSerializer, TCListSerializer
from .models import Course, Quizz, TeacherCourse


@api_view(["GET"])
def get_courses(request):
    tc = TeacherCourse.objects.filter(teacher_id=request.user.id).select_related('course')
    data = []
    if request.user.is_authenticated:
        for item in tc:
            data.append({'id':item.course.id, 'title':item.course.title, 'slug': item.course.slug, 'short_description': item.course.short_description, 'long_description': item.course.long_description})
    return Response(data)

@api_view(["GET"])
def get_course(request, slug):
    course = Course.objects.get(slug=slug)
    quizz = Quizz.objects.filter(course_id=course.id)
    serializer = CourseListSerializer(course)
    quizz_serializer = QuizzListSerializer(quizz, many=True)
    if request.user.is_authenticated:
        data = Response({
        'course': serializer.data,
        'quizzes': quizz_serializer.data
    })
    else:
        data = Response({})
    return data

@api_view(["GET"])
def get_quiz(request, slug):
    course = Course.objects.get(slug=slug)
    quizz = Quizz.objects.filter(course_id=course.id)
    serializer = CourseListSerializer(course)
    quizz_serializer = QuizzListSerializer(quizz, many=True)
    headlist = []
    for field in QuizzListSerializer.Meta.fields:
        headlist.append({'row': field})
    if request.user.is_authenticated:
        data = Response({
        'headlist': headlist,
        'course': serializer.data,
        'quizzes': quizz_serializer.data
    })
    else:
        data = Response({})
    return data