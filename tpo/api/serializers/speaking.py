from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField


class SpeakingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    speaking_audio_file = serializers.SerializerMethodField()
    speaking_reading_title = serializers.CharField()
    speaking_reading = serializers.CharField()
    speaking_reading_time = serializers.IntegerField()
    speaking_time = serializers.IntegerField()
    speaking_prepare_time = serializers.IntegerField()
    speaking_image = serializers.SerializerMethodField()
    speaking_question = serializers.CharField()
    speaking_question_audio_file = serializers.SerializerMethodField()
    speaking_question_guide_audio_file = serializers.SerializerMethodField()
    speaking_question_before_read_audio = serializers.SerializerMethodField()
    number = serializers.IntegerField()

    def get_speaking_audio_file(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.speaking_audio_file)

    def get_speaking_image(self, model):
        return 'data:image;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.speaking_image)

    def get_speaking_question_audio_file(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.speaking_question_audio_file)

    def get_speaking_question_guide_audio_file(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.speaking_question_guide_audio_file)

    def get_speaking_question_before_read_audio(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.speaking_question_before_read_audio)

