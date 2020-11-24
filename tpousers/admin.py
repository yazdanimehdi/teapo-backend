from django.contrib import admin
from tpousers.models import TestUser, OrderPendingPayment, UserWritingCorrectionOrder, UserSpeakingCorrectionOrder, \
    UserSpeakingAnswers, UserWritingAnswers, GlobalVariables

# Register your models here.
admin.site.register(TestUser)
admin.site.register(OrderPendingPayment)
admin.site.register(UserWritingCorrectionOrder)
admin.site.register(UserSpeakingCorrectionOrder)
admin.site.register(UserSpeakingAnswers)
admin.site.register(UserWritingAnswers)
admin.site.register(GlobalVariables)
