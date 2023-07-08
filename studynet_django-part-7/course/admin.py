from django.contrib import admin

# Register your models here.
from .models import Course, Quizz, TeacherCourse

admin.site.register(Course)
admin.site.register(Quizz)
admin.site.register(TeacherCourse)