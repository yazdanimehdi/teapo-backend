from rest_framework import serializers
from tpousers.models import UserWritingCorrectionOrder, UserSpeakingCorrectionOrder


class UserWritingCorrectionOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserWritingCorrectionOrder
        exclude = ('user', 'writing_answer', )


class UserSpeakingCorrectionOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSpeakingCorrectionOrder
        exclude = ('user', 'speaking_answers', )

