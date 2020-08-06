import base64
import os
import random
import re
import string

import requests
import json
from django.conf import settings
from django.core.files import File
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpousers.models import UserWritingCorrectionOrder, UserSpeakingCorrectionOrder, SpeakingOrderPendingPayment, \
    WritingOrderPendingPayment, UserSpeakingAnswers, TestUser, GlobalVariables

from tpo.models import Test, Speaking
from rest_framework import status
from django.utils.timezone import now


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def order_speaking_correction(request):
    test_id = request.data[1]
    user_test = TestUser()
    try:
        user_test.test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user_test.user = request.user
    user_test.date_time = now()
    user_test.is_done = True

    answers = request.data[0]
    order = UserSpeakingCorrectionOrder()
    order.user = request.user
    order.save()
    for item in answers:
        user_speaking_answer, created = UserSpeakingAnswers.objects.get_or_create(
            question=Speaking.objects.get(id=item),
            user_test=user_test,
        )

        user_speaking_answer.user_test = user_test
        user_speaking_answer.question = Speaking.objects.get(id=item)
        string_encoded = answers[item]
        string_encoded = re.sub(r'data:audio/webm;codecs=opus;base64,', '', string_encoded)
        b = bytes(string_encoded, 'utf-8')
        if b.__len__() % 4 != 0:
            c = [b'=' for i in range(b.__len__() % 4)]
            correcting = b''
            for eq in c:
                correcting += eq
            print(correcting)
            b = b + correcting
        print(b.__len__() % 4)
        decoded = base64.decodebytes(b)

        speaking_file = open(f'{item}.webm', 'wb')
        speaking_file.write(decoded)
        speaking_file.close()
        file = open(f'{item}.webm', 'rb')
        djangofile = File(file)
        user_speaking_answer.answer = File(djangofile)
        user_speaking_answer.save()
        os.remove(f'{item}.webm')
        order.speaking_answers.add(user_speaking_answer)

    price = int(GlobalVariables.objects.get(key='SpeakingPrice').value)
    payment = SpeakingOrderPendingPayment()
    payment.order = order
    letters = string.ascii_lowercase
    digits = string.digits
    payment.token = ''.join(random.choice(letters + digits) for i in range(20))
    payment.fee = price
    payment.save()

    headers = {'X-API-KEY': settings.PAY_API_KEY, 'X-SANDBOX': '1', 'Content-Type': 'application/json'}
    data = {
      "order_id": payment.token,
      "amount": payment.fee,
      "name": request.user.last_name,
      "phone": request.user.phone,
      "mail": request.user.email,
      "callback": "https://teapo.ir/verify"
    }
    response = requests.post(url='https://api.idpay.ir/v1.1/payment', data=json.dumps(data), headers=headers)
    return Response(data=response.json(), status=status.HTTP_200_OK)


