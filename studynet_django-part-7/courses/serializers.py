from rest_framework import serializers

from .models import Course, Chapter, Quiz, Muliplechoicesanswer, Teachercourse

class CourseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

class ChapterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = '__all__'

class QuizListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'

class MCAListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Muliplechoicesanswer
        fields = '__all__'

class TCListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teachercourse
        fields = '__all__'

class ListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['multichoice'] = MCAListSerializer(instance.multianswers.filter(question_id=instance.id).first()).data
        representation['Chapter'] = instance.chapter_id.title
        return representation