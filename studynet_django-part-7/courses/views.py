from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError

from .serializers import CourseListSerializer, ChapterListSerializer, TCListSerializer, QuizListSerializer, TCListSerializer, ListViewSerializer
from .models import Course, Chapter, Quiz, Muliplechoicesanswer, Teachercourse
from .filters import QuizFilter

@api_view(["GET"])
def get_courses(request):
    if request.user.is_authenticated:
        tc = Teachercourse.objects.filter(teacher_id=request.user.id).select_related('course_id')
        data = []
        for item in tc:
            data.append({'id':item.course_id.id, 'title':item.course_id.title, 'slug': item.course_id.slug, 'short_description': item.course_id.short_description, 'long_description': item.course_id.long_description})
        return Response(data)

    else:
        data = []
    return Response(data)

@api_view(["GET"])
def get_course(request, slug):
    course = Course.objects.get(slug=slug)
    serializer = CourseListSerializer(course)
    if request.user.is_authenticated:
        data = Response({
        'course': serializer.data,
    })
    else:
        data = Response({})
    return data

@api_view(["GET"])
def get_quiz(request, slug):
    course = Course.objects.get(slug=slug)
    quiz = Quiz.objects.select_related().prefetch_related().filter(chapter_id__course_id__id=course.id)
    serializer = CourseListSerializer(course)
    quiz_serializer = ListViewSerializer(quiz, many=True)
    if request.user.is_authenticated:
        data = Response({
        'course': serializer.data,
        'quizzes': quiz_serializer.data
    })
    else:
        data = Response({})
    return data

@api_view(["DELETE"])
def delete_quiz(request, slug, id):
    if request.user.is_authenticated:
        course = Course.objects.get(slug=slug)
        quiz = Quiz.objects.get(id=id)
        quiz.delete()
        return Response("Success", status=status.HTTP_200_OK)
        #except:
            #return Response("Quiz doesn't match the course", status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def edit_quiz(request, slug):
    if request.user.is_authenticated:
        course = Course.objects.get(slug=slug)
        data = request.data
        qid = data.pop("id")
        cid = data.pop("chapter_id")
        multichoice = data.pop("multichoice")
        _ = data.pop("created_at")
        chapter_name = data.pop("Chapter")
        try:
            chapter = Chapter.objects.get(title=chapter_name, course_id=course.id)
            data["chapter_id"] = chapter
        except Chapter.DoesNotExist:
            return Response("The chapter doesn't exist. Contact the admin to add the chapter", status=status.HTTP_404_NOT_FOUND)
        
        Quiz.objects.filter(pk=qid).update(**data)
        
        if multichoice["question_id"]:
            _ = multichoice.pop("question_id")
            Muliplechoicesanswer.objects.filter(question_id=qid).update(**multichoice)
        return Response("Success", status=status.HTTP_200_OK)

@api_view(["GET"])
def filter_quiz(request, slug):
    if request.user.is_authenticated:
        course = Course.objects.get(slug=slug)
        data = request.data
        quiz = Quiz.objects.select_related().prefetch_related().filter(chapter_id__course_id__id=course.id)
        quiz = QuizFilter(request.GET, queryset=quiz)
        if quiz.is_valid():
            quiz = quiz.qs
        print(quiz)
        serializer = ListViewSerializer(quiz, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def insert_quiz(request, slug):
    if request.user.is_authenticated:
        course = Course.objects.get(slug=slug)
        data = request.data
        try:
            chapter_name = data.pop("Chapter")
            chapter = Chapter.objects.get(title=chapter_name, course_id=course.id)
            data["chapter_id"] = chapter
            answer1 = data.pop("Answer 1")
            answer2 = data.pop("Answer 2")
            answer3 = data.pop("Answer 3")
            answer4 = data.pop("Answer 4")
            added = Quiz.objects.create(**data)
            if data["qtype"] == "multichoices":
                multi = {}
                multi["question_id"] = added
                multi["answer1"] = answer1
                multi["answer2"] = answer2
                multi["answer3"] = answer3
                multi["answer4"] = answer4
                Muliplechoicesanswer.objects.create(**multi)
            return Response("Success", status=status.HTTP_200_OK)

        except Chapter.DoesNotExist:
            return Response("The chapter doesn't exist. Contact the admin to add the chapter", status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response("Wrong data input type", status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response("Wrong data input type", status=status.HTTP_404_NOT_FOUND)