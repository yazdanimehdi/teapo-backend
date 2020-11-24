import json

import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from institutions.models import Users
from tpousers.models import OrderPendingPayment, MockPendingPayment, UserSpeakingCorrectionOrder, \
    UserWritingCorrectionOrder, TestUser
import datetime
from django.shortcuts import render, Http404


@csrf_exempt
def correction_verification(request):
    if request.META.get('HTTP_ORIGIN') == 'https://idpay.ir' and request.method == 'POST':
        status_code = request.POST.get('status')
        track_id = request.POST.get('track_id')
        tr_id = request.POST.get('id')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        card_no = request.POST.get('card_no')
        date = request.POST.get('date')

        headers = {'X-API-KEY': settings.PAY_API_KEY,
                   'X-SANDBOX': '1',
                   'Content-Type': 'application/json'}

        if status_code == '10':
            try:
                transaction = OrderPendingPayment.objects.get(token=order_id, transaction_id=tr_id, fee=amount,
                                                              status=False)
            except OrderPendingPayment.DoesNotExist:
                return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})

            data = {
                'id': tr_id,
                'order_id': order_id,
            }

            response = requests.post(url='https://api.idpay.ir/v1.1/payment/verify', data=json.dumps(data),
                                     headers=headers)
            if response.status_code == 200:

                corrector_list = []

                for corrector in Users.objects.filter(role=3, accept_correction=True):
                    speaking_orders = UserSpeakingCorrectionOrder.objects.filter(assigned_corrector=corrector)
                    writing_orders = UserWritingCorrectionOrder.objects.filter(assigned_corrector=corrector)
                    not_done = len(TestUser.objects.filter(assigned_corrector=corrector, is_corrected=False))
                    rating = 0
                    number = 0

                    for item in speaking_orders:
                        if item.state == 0:
                            not_done += 1

                        if item.user_rating is not None:
                            rating += item.user_rating
                            number += 1

                    for item in writing_orders:
                        if item.state == 0:
                            not_done += 1

                        if item.user_rating is not None:
                            rating += item.user_rating
                            number += 1
                    if corrector.active_correction_limit - not_done > 0:
                        corrector_list.append([corrector, rating, corrector.active_correction_limit - not_done])

                transaction.status = True
                transaction.card_no = card_no
                transaction.date = datetime.datetime.fromtimestamp(date)
                transaction.track_id = track_id
                transaction.save()
                if transaction.order_speaking is not None:
                    transaction.order_speaking.is_paid = True
                    if corrector_list.__len__() != 0:
                        corrector_list.sort(key=lambda x: (-x[1], -x[2]))
                        transaction.order_speaking.assigned_corrector = corrector_list[0][0]
                        if corrector_list[0][2] - 1 > 0:
                            corrector_list[0][2] -= 1
                        else:
                            corrector_list.pop(0)
                    transaction.order_speaking.save()
                if transaction.order_writing is not None:
                    if corrector_list.__len__() != 0:
                        corrector_list.sort(key=lambda x: (-x[1], -x[2]))
                        transaction.order_writing.assigned_corrector = corrector_list[0][0]
                    transaction.order_writing.is_paid = True
                    transaction.order_writing.save()
                return render(request, 'tpousers/transaction_result.html', {'transaction_status': True})
            else:
                return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})

        else:
            return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})
    else:
        return Http404


@csrf_exempt
def mock_verification(request):
    if request.META.get('HTTP_ORIGIN') == 'https://idpay.ir' and request.method == 'POST':
        status_code = request.POST.get('status')
        track_id = request.POST.get('track_id')
        tr_id = request.POST.get('id')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        card_no = request.POST.get('card_no')
        date = request.POST.get('date')

        headers = {'X-API-KEY': settings.PAY_API_KEY,
                   'X-SANDBOX': '1',
                   'Content-Type': 'application/json'}

        if status_code == '10':
            try:
                transaction = MockPendingPayment.objects.get(token=order_id, transaction_id=tr_id, fee=amount,
                                                             status=False)
            except OrderPendingPayment.DoesNotExist:
                return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})

            data = {
                'id': tr_id,
                'order_id': order_id,
            }

            response = requests.post(url='https://api.idpay.ir/v1.1/payment/verify', data=json.dumps(data),
                                     headers=headers)
            if response.status_code == 200:
                transaction.status = True
                transaction.card_no = card_no
                transaction.date = datetime.datetime.fromtimestamp(date)
                transaction.track_id = track_id
                transaction.save()
                transaction.test_user.is_paid = True
                transaction.test_user.save()

                return render(request, 'tpousers/transaction_result.html', {'transaction_status': True})
            else:
                return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})

        else:
            return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})
    else:
        return Http404
