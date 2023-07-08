from django.db import models
from django.conf import settings

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)


class Quizz(models.Model):
    course = models.ForeignKey(Course, related_name="quizzes", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    qtype = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)


class TeacherCourse(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="teacher", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="course", on_delete=models.CASCADE)
