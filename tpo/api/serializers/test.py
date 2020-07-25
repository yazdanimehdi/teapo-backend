from rest_framework import serializers
from tpo.api.serializers import WritingSerializer, ReadingSerializer, SpeakingSerializer, ListeningSerializer
from tpo.models import Speaking, Reading, Writing, Listening


class TestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    speaking = serializers.SerializerMethodField()
    reading = serializers.SerializerMethodField()
    listening = serializers.SerializerMethodField()
    writing = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    def get_time(self, model):
        return TestTimeSerializer(model.test).data

    def get_speaking(self, model):
        return [SpeakingSerializer(x).data for x in Speaking.objects.filter(testspeaking__test=model.test).order_by('number')]

    def get_writing(self, model):
        return [WritingSerializer(x).data for x in Writing.objects.filter(testwriting__test=model.test)]

    def get_listening(self, model):
        return [ListeningSerializer(x).data for x in Listening.objects.filter(testlistening__test=model.test)]

    def get_reading(self, model):
        return [ReadingSerializer(x).data for x in Reading.objects.filter(testreading__test=model.test)]


class TestTimeSerializer(serializers.Serializer):
    listening_time = serializers.IntegerField()
    reading_time = serializers.IntegerField()