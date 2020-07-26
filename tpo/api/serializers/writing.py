from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField
from tpo.models import WritingTimes


class WritingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    writing_listening = serializers.SerializerMethodField()
    writing_image = serializers.SerializerMethodField()
    writing_reading = serializers.CharField()
    writing_question = serializers.CharField()
    type = serializers.CharField()
    writing_listening_transcript = serializers.CharField()
    section = serializers.IntegerField()
    sections = serializers.IntegerField()

    def get_writing_listening(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.writing_listening)

    def get_writing_image(self, model):
        return 'data:image;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.writing_image)


class WritingTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTimes
        fields = '__all__'