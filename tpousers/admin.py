from django.contrib import admin
from tpousers.models import TestUser, OrderPendingPayment, UserWritingCorrectionOrder, UserSpeakingCorrectionOrder, \
    UserSpeakingAnswers, UserWritingAnswers

# Register your models here.
admin.site.register(TestUser)
admin.site.register(OrderPendingPayment)
admin.site.register(UserWritingCorrectionOrder)
admin.site.register(UserSpeakingCorrectionOrder)
admin.site.register(UserSpeakingAnswers)
admin.site.register(UserWritingAnswers)

