from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
class Course(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    long_description = models.TextField()
    created_at = models.DateField(auto_now_add=True)

class Chapter(models.Model):

    title = models.CharField(max_length=255)
    course_id = models.ForeignKey(Course, to_field="id", related_name="chapter", on_delete=models.CASCADE)
    chapter_content = models.TextField()

class Quiz(models.Model):

    MULTICHOICE = 'multichoices'
    TF = 'T/F'
    PARAGRAPH = 'paragraph'
    TYPE_Q = (
        (MULTICHOICE, 'multichoices'),
        (TF, 'T/F'),
        (PARAGRAPH, 'PARAGRAPH')
    )

    chapter_id = models.ForeignKey(Chapter, to_field="id", related_name="quiz", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    qtype = models.TextField(choices=TYPE_Q, null=False, blank=False)
    avgtime = models.FloatField()
    level = models.FloatField()
    answer = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def clean(self):
        # Perform data type validation or cleaning here
        # Example: Ensure name is a string and trim any leading/trailing whitespace
        print(self.qtype)
        if not(self.qtype == self.TF or self.qtype == self.PARAGRAPH or self.qtype == self.MULTICHOICE):
            raise ValidationError('')
        super(Quiz, self).clean()

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)

class Muliplechoicesanswer(models.Model):

    question_id = models.ForeignKey(Quiz, to_field="id", related_name="multianswers", on_delete=models.CASCADE)
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    answer4 = models.CharField(max_length=255)

class Teachercourse(models.Model):

    teacher_id = models.ForeignKey(settings.AUTH_USER_MODEL, to_field="id", related_name="teacher", on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, to_field="id", related_name="course", on_delete=models.CASCADE)
