from django.contrib import admin

# Register your models here.
from .models import Course, Chapter, Quiz, Muliplechoicesanswer, Teachercourse

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Quiz)
admin.site.register(Teachercourse)
admin.site.register(Muliplechoicesanswer)
