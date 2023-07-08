from django.urls import path

from course import views

urlpatterns = [
    path('', views.get_courses),
    path('<slug:slug>/', views.get_course),
    path('<slug:slug>/get-quizzes', views.get_quiz)
]