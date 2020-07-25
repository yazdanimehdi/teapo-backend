from tpo.models import ReadingQuestions, ReadingAnswers
from rest_framework import serializers


class ReadingAnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadingAnswers
        fields = '__all__'


class ReadingQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    number = serializers.IntegerField()
    insertion_sentence = serializers.CharField()
    related_paragraph = serializers.IntegerField()
    related_passage = serializers.CharField()
    question_type = serializers.CharField()
    reading = serializers.IntegerField(source='reading.pk')
    answers = serializers.SerializerMethodField()
    right_answer = serializers.CharField()

    def get_answers(self, model):
        return [ReadingAnswersSerializer(x).data for x in ReadingAnswers.objects.filter(question=model)]


class ReadingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    passage = serializers.CharField()
    questions = serializers.SerializerMethodField()

    def get_questions(self, model):
        return [ReadingQuestionSerializer(x).data for x in ReadingQuestions.objects.filter(reading=model).order_by('number')]




