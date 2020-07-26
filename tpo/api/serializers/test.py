from rest_framework import serializers
from tpo.api.serializers import WritingSerializer, ReadingSerializer, SpeakingSerializer, ListeningSerializer, \
    ListeningTimesSerializer, WritingTimesSerializer, SpeakingTimesSerializer
from tpo.models import Speaking, Reading, Writing, Listening, Test, SpeakingTimes, ListeningTimes, WritingTimes, \
    TestListening
from tpousers.models import TestUser


class TestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    reading_time = serializers.IntegerField()
    title = serializers.CharField()
    code = serializers.CharField()
    mode = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    deadline = serializers.DateTimeField()
    class_assigned_id = serializers.SerializerMethodField()
    institute_id = serializers.SerializerMethodField()

    speaking = serializers.SerializerMethodField()
    reading = serializers.SerializerMethodField()
    listening = serializers.SerializerMethodField()
    writing = serializers.SerializerMethodField()
    speaking_times = serializers.SerializerMethodField()
    listening_times = serializers.SerializerMethodField()
    writing_times = serializers.SerializerMethodField()

    def get_institute_id(self, model):
        if model.institute is None:
            return None
        else:
            return model.institute.id

    def get_class_assigned_id(self, model):
        if model.class_assigned is None:
            return None
        else:
            return model.class_assigned.id

    def get_speaking_times(self, model):
        return [SpeakingTimesSerializer(x).data for x in SpeakingTimes.objects.filter(test=model).order_by('number')]

    def get_listening_times(self, model):
        return [ListeningTimesSerializer(x).data for x in ListeningTimes.objects.filter(test=model).order_by('number')]

    def get_writing_times(self, model):
        return [WritingTimesSerializer(x).data for x in WritingTimes.objects.filter(test=model).order_by('number')]

    def get_speaking(self, model):
        return [SpeakingSerializer(x).data for x in
                Speaking.objects.filter(testspeaking__test=model).order_by('number')]

    def get_writing(self, model):
        return [WritingSerializer(x).data for x in Writing.objects.filter(testwriting__test=model)]

    def get_listening(self, model):
        try:
            return [{'listening': ListeningSerializer(x).data,
                     'phase': TestListening.objects.get(test_id=model.id, listening_id=x.id).phase,
                     'part': TestListening.objects.get(test_id=model.id, listening_id=x.id).part} for x in
                    Listening.objects.filter(testlistening__test=model)]
        except TestListening.DoesNotExist:
            return []

    def get_reading(self, model):
        return [ReadingSerializer(x).data for x in Reading.objects.filter(testreading__test=model)]


class TPOListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    code = serializers.CharField()
    mode = serializers.CharField()
    paid = serializers.SerializerMethodField()

    def get_paid(self, model):
        return TestUser.objects.filter(is_paid=True, test=model).__len__() != 0 if model.mode == 'P' else True


class MockListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    code = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()


class AssignmentListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    code = serializers.CharField()
    deadline = serializers.DateTimeField()
