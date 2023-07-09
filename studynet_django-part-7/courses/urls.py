from django.urls import path

from courses import views

urlpatterns = [
    path('', views.get_courses),
    path('<slug:slug>/', views.get_course),
    path('<slug:slug>/get-quizzes/', views.get_quiz),
    path('<slug:slug>/delete-quiz/<int:id>/', views.delete_quiz),
    path('<slug:slug>/edit-quizzes/', views.edit_quiz),
    path('<slug:slug>/filter-quiz/', views.filter_quiz),
    path('<slug:slug>/insert-quiz/', views.insert_quiz),
    path('<slug:slug>/get-chapter/', views.get_chapter),
    path('<slug:slug>/gen-exam/', views.gen_exam)
]