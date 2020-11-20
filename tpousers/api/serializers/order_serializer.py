from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers
from tpousers.models import UserSpeakingCorrectionOrder, UserWritingAnswers, UserSpeakingAnswers


class UserWritingCorrectionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserWritingAnswers
        exclude = ('user_test',)


class UserSpeakingCorrectionAnswerSerializer(serializers.SerializerMethodField):

    question = serializers.IntegerField()
    answer = serializers.SerializerMethodField()

    def get_answer(self, model):
        return 'data:audio/mpeg;base64,' + Base64FileField(represent_in_base64=True).to_representation(
            model.answer)


class UserWritingCorrectionOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    test_id = serializers.SerializerMethodField()
    local_user_test_id = serializers.IntegerField()
    date = serializers.SerializerMethodField()
    writing_answers = serializers.SerializerMethodField()
    assigned_corrector = serializers.SerializerMethodField()
    score = serializers.IntegerField()
    comment = serializers.CharField()
    related_file = serializers.FileField()
    state = serializers.IntegerField()
    is_paid = serializers.BooleanField()
    user_review = serializers.CharField()
    user_rating = serializers.IntegerField()

    def get_writing_answers(self, model):
        return [UserWritingCorrectionAnswerSerializer(x).data for x in model.writing_answer.all()]

    def get_assigned_corrector(self, model):
        return str(model.assigned_corrector.first_name + model.assigned_corrector.last_name)

    def get_test_id(self, model):
        return model.writing_answer.all()[0].user_test.test.id

    def get_date(self, model):
        return int(model.writing_answer.all()[0].user_test.date_time.timestamp()) * 1000


class UserSpeakingCorrectionOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    test_id = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    local_user_test_id = serializers.IntegerField()
    speaking_answers = serializers.SerializerMethodField()
    assigned_corrector = serializers.SerializerMethodField()
    score = serializers.IntegerField()
    comment = serializers.CharField()
    related_file = serializers.FileField()
    state = serializers.IntegerField()
    is_paid = serializers.BooleanField()
    user_review = serializers.CharField()
    user_rating = serializers.IntegerField()

    def get_speaking_answers(self, model):
        return [UserSpeakingCorrectionAnswerSerializer(x).data for x in model.speaking_answers.all()]

    def get_assigned_corrector(self, model):
        return str(model.assigned_corrector.first_name + model.assigned_corrector.last_name)

    def get_test_id(self, model):
        return model.writing_answer.all()[0].user_test.test.id

    def get_date(self, model):
        return int(model.writing_answer.all()[0].user_test.date_time.timestamp()) * 1000
