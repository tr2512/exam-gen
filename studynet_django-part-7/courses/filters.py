from .models import Quiz
import django_filters

class QuizFilter(django_filters.FilterSet):

    content = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Quiz
        fields = ['content']