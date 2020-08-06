from abc import ABC

from tpo.models import ListeningQuestions, ListeningAnswers, ListeningTimes, TestListening
from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField


class ListeningAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningAnswers
        fields = '__all__'


class ListeningQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    number = serializers.IntegerField()
    quote = serializers.BooleanField()
    listening_question_audio_file = serializers.SerializerMethodField()
    quote_audio_file = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    right_answer = serializers.CharField()

    def get_listening_question_audio_file(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(model.listening_question_audio_file)

    def get_quote_audio_file(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.quote_audio_file)

    def get_answers(self, model):
        return [ListeningAnswersSerializer(x).data for x in ListeningAnswers.objects.filter(question=model)]


class ListeningSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    listening = serializers.SerializerMethodField()
    listening_image = serializers.SerializerMethodField()
    title = serializers.CharField()
    type = serializers.CharField()
    transcript = serializers.CharField()
    questions = serializers.SerializerMethodField()

    def get_questions(self, model):
        return [ListeningQuestionSerializer(x).data for x in ListeningQuestions.objects.filter(listening=model).order_by('number')]

    def get_listening(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.listening)

    def get_listening_image(self, model):
        return 'data:image;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.listening_image)


class ListeningTimesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListeningTimes
        fields = '__all__'

