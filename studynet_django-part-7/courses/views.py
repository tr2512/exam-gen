from django.shortcuts import render

# Create your views here.
from django.http import FileResponse, HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
import pandas as pd

from .serializers import CourseListSerializer, ChapterListSerializer, TCListSerializer, QuizListSerializer, TCListSerializer, ListViewSerializer
from .models import Course, Chapter, Quiz, Muliplechoicesanswer, Teachercourse
from .filters import QuizFilter
from .utils import generate_questions
import random
from django.contrib.auth.decorators import login_required, user_passes_test
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
import json

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

@api_view(["GET"])
def get_chapter(request, slug):
    if request.user.is_authenticated:
        course = Course.objects.get(slug=slug)
        chapters = Chapter.objects.filter(course_id=course)
        chapters_se = ChapterListSerializer(chapters, many=True)
        data = chapters_se.data
    else:
        data = []
    return Response(data)

@api_view(["GET"])
def gen_exam(request, slug):
    course = Course.objects.get(slug=slug)
    print(type(request.GET.get("content")))
    data = eval(request.GET.get("content").replace('true', "True").replace("false", "False"))
    diff = float(data["avg_diff"])
    print(diff)
    duration = 0
    index = 0
    while not (duration > float(data["min_duration"]) and duration < float(data["max_duration"])):
        duration = 0
        index += 1
        quizzes = Quiz.objects.select_related().prefetch_related().filter(chapter_id__course_id__id=course.id)
        d = {i: {j: None for j in data["chapters"].keys() if data["chapters"][j]} for i in data["qtype"] if int(data["qtype"][i]) > 0}
        d_final = {i:[] for i in data["qtype"] if int(data["qtype"][i]) > 0}
        for keyi in d.keys():
            for keyj in d[keyi].keys():
                print(keyi, keyj)
                quiz = Quiz.objects.filter(chapter_id=keyj, level__gt=diff - 2.5, level__lt=diff + 2.5, qtype=keyi).values()
                print(list(quiz))
                d[keyi][keyj] = random.sample(list(quiz), int(data["qtype"][keyi]))
                d_final[keyi] += d[keyi][keyj]
            d_final[keyi] = random.sample(d_final[keyi], int(data["qtype"][keyi]))
            for i in d_final[keyi]:
                duration += i['avgtime']
        if index == 5:
            return Response("FAIL", status=status.HTTP_404_NOT_FOUND)
    

    lines = []
    i = 0
    print(d_final)
    for key, value in d_final.items():
        for q in value:
            i += 1
            qcontent = q["content"]
            question = f"Question {i}: {qcontent} <br/>"
            lines.append(question)
            lines.append(" ")
            if key == "multichoices":
                print(int(q["id"]))
                answer = Muliplechoicesanswer.objects.get(question_id=int(q["id"]))
                lines.append(f"A. {answer.answer1}")
                lines.append(f"B. {answer.answer2}")
                lines.append(f"C. {answer.answer3}")
                lines.append(f"D. {answer.answer4}")
                lines.append(" ")
    
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="example.pdf"'

    document = SimpleDocTemplate(response, pagesize=letter)

    content = []

    styles = getSampleStyleSheet()

    for line in lines:
        if line == " ":
            content.append(Spacer(1, 12))
        else:
            content.append(Paragraph(line, styles['Normal']))

    document.build(content)

    return response


@api_view(["POST"])
def upload_csv(request, slug):
    if request.user.is_authenticated:
        csv_file = request.FILES.get('file')
        df = pd.read_csv(csv_file)
        df1 = df.groupby(["Question_name"], as_index=False).mean()
        print(df1.keys())
        qname = []
        true_time = []
        avg_score = []
        t_db = 0
        for index, row in df1.iterrows():
            name = row["Question_name"]
            qname.append(name)
            q = Quiz.objects.filter(content=name).first()
            true_time.append(q.avgtime)
            t = row["Time"]
            t_db += q.avgtime
            avg_score.append(row["Score"])
        relative_time = [time * t / t_db for time in true_time]
        new_time = [0.9 * t_true + 0.1 * t_relative / ascore for t_true, t_relative, ascore in zip(true_time, relative_time, avg_score)]
        for name, t in zip(qname, new_time):
            Quiz.objects.filter(content=name).update(avgtime=t)
        return Response("Succesful update", status=status.HTTP_200_OK)