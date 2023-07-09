from django.urls import path
from courses import views

urlpatterns = [
    path('course/', views.get_courses),
    path('course/<slug:slug>/', views.get_course),
    path('course/<slug:slug>/get-quizzes/', views.get_quiz),
    path('course/<slug:slug>/delete-quiz/<int:id>/', views.delete_quiz),
    path('course/<slug:slug>/edit-quizzes/', views.edit_quiz),
    path('course/<slug:slug>/filter-quiz/', views.filter_quiz),
    path('course/<slug:slug>/insert-quiz/', views.insert_quiz),
    path('course/<slug:slug>/get-chapter/', views.get_chapter),
    path('course/<slug:slug>/gen-exam/', views.gen_exam), 
    path('course/<slug:slug>/upload-csv/', views.upload_csv),
    path('verify/', views.get_user_group),
    path('get-teachers/', views.get_user),
    path('create-course/', views.create_course),
    path('delete-course/', views.delete_course),
    path('<slug:slug>/teachers/', views.get_teachers),
    path('<slug:slug>/edit-course/', views.edit_course)
]