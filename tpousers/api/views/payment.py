import base64
import os
import random
import re
import string
from datetime import datetime

import requests
import json
from django.conf import settings
from django.core.files import File
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpousers.models import UserWritingCorrectionOrder, UserSpeakingCorrectionOrder, OrderPendingPayment, \
    UserSpeakingAnswers, TestUser, GlobalVariables, UserWritingAnswers, MockPendingPayment

from tpo.models import Test, Speaking, Writing
from rest_framework import status
from django.utils.timezone import now


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def order_correction(request):
    price_writing = int(GlobalVariables.objects.get(key='WritingPrice').value)
    price_speaking = int(GlobalVariables.objects.get(key='SpeakingPrice').value)
    payment = OrderPendingPayment()

    speaking_order_list = OrderPendingPayment.objects.filter(order_speaking__local_user_test_id=request.data[3],
                                                             order_speaking__user=request.user,
                                                             order_speaking__is_paid=False)
    writing_order_list = OrderPendingPayment.objects.filter(order_writing__local_user_test_id=request.data[3],
                                                            order_writing__user=request.user,
                                                            order_writing__is_paid=False)
    if (request.data[0] and speaking_order_list.__len__() == 0) or (
            request.data[1] and writing_order_list.__len__() == 0):
        test_id = request.data[2]
        user_test = TestUser()
        try:
            user_test.test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_test.user = request.user
        user_test.date_time = now()
        user_test.is_done = True
        user_test.save()

    if request.data[0]:
        if speaking_order_list.__len__() == 0:
            answers = request.data[0]
            order = UserSpeakingCorrectionOrder()
            order.user = request.user
            order.local_user_test_id = request.data[3]
            order.save()
            for item in answers:
                user_speaking_answer = UserSpeakingAnswers()
                user_speaking_answer.question = Speaking.objects.get(id=item['question_id'])
                user_speaking_answer.user_test = user_test
                string_encoded = item['answer']
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

                speaking_file = open(f'{item["id"]}.webm', 'wb')
                speaking_file.write(decoded)
                speaking_file.close()
                file = open(f'{item["id"]}.webm', 'rb')
                djangofile = File(file)
                user_speaking_answer.answer = File(djangofile)
                user_speaking_answer.save()
                os.remove(f'{item["id"]}.webm')
                order.speaking_answers.add(user_speaking_answer)
            payment.order_speaking = order
        else:
            payment.order_speaking = speaking_order_list[0].order_speaking
            speaking_order_list[0].order_speaking = None

    if request.data[1]:
        if writing_order_list.__len__() == 0:
            order_writing = UserWritingCorrectionOrder()
            order_writing.local_user_test_id = request.data[3]
            order_writing.user = request.user
            order_writing.save()
            writing_answers = request.data[1]
            for item in writing_answers:
                user_writing_answer = UserWritingAnswers()
                user_writing_answer.question = Writing.objects.get(id=item['question_id'])
                user_writing_answer.user_test = user_test
                user_writing_answer.answer = item['answer']
                user_writing_answer.save()
                order_writing.writing_answer.add(user_writing_answer)

            payment.order_writing = order_writing
        else:
            payment.order_writing = writing_order_list[0].order_writing
            writing_order_list[0].order_writing = None

    for item in speaking_order_list:
        if item.order_speaking is None and item.order_writing is None:
            item.delete()

    for item in speaking_order_list:
        if item.order_speaking is None and item.order_writing is None:
            try:
                item.delete()
            except Exception:
                pass

    letters = string.ascii_lowercase
    digits = string.digits
    payment.token = ''.join(random.choice(letters + digits) for i in range(20))
    total_price = 0
    if len(request.data[0]) != 0:
        total_price += price_speaking
    if len(request.data[1]) != 0:
        total_price += price_writing

    payment.fee = total_price

    headers = {'X-API-KEY': settings.PAY_API_KEY, 'X-SANDBOX': '1', 'Content-Type': 'application/json'}
    data = {
        "order_id": payment.token,
        "amount": payment.fee * 10,
        "name": request.user.last_name,
        "phone": request.user.phone,
        "mail": request.user.email,
        "callback": "https://main.teapo.ir/verify/order/correction"
    }
    response = requests.post(url='https://api.idpay.ir/v1.1/payment', data=json.dumps(data), headers=headers)

    payment.transaction_id = response.json()['id']
    payment.save()

    return Response(data=response.json(), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def order_mock(request):
    user = request.user
    test_id = request.data['id']
    try:
        test_user = TestUser.objects.get(user=user, test__id=test_id)
    except TestUser.DoesNotExist:
        test_user = TestUser()
        test_user.user = user
        test_user.date_time = now()

        try:
            test_user.test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_user.is_paid = False
        test_user.save()

    payment = MockPendingPayment()
    payment.test_user = test_user
    payment.fee = test_user.test.fee
    letters = string.ascii_lowercase
    digits = string.digits
    payment.token = ''.join(random.choice(letters + digits) for i in range(20))

    headers = {'X-API-KEY': settings.PAY_API_KEY, 'X-SANDBOX': '1', 'Content-Type': 'application/json'}
    data = {
        "order_id": payment.token,
        "amount": payment.fee * 10,
        "name": request.user.last_name,
        "phone": request.user.phone,
        "mail": request.user.email,
        "callback": "https://main.teapo.ir/verify/order/mock"
    }
    response = requests.post(url='https://api.idpay.ir/v1.1/payment', data=json.dumps(data), headers=headers)

    payment.transaction_id = response.json()['id']
    payment.save()

    return Response(data=response.json(), status=status.HTTP_200_OK)