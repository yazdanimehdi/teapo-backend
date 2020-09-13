import json

import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from tpousers.models import OrderPendingPayment
import datetime
from django.shortcuts import render


@csrf_exempt
def correction_verification(request):
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
            transaction = OrderPendingPayment.objects.get(token=order_id, transaction_id=tr_id, fee=amount)
        except OrderPendingPayment.DoesNotExist:
            return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})

        data = {
            'id': tr_id,
            'order_id': order_id,
        }

        response = requests.post(url='https://api.idpay.ir/v1.1/payment/verify', data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            transaction.status = True
            transaction.card_no = card_no
            transaction.date = datetime.datetime.fromtimestamp(date)
            transaction.track_id = track_id
            transaction.save()
            if transaction.order_speaking is not None:
                transaction.order_speaking.is_paid = True
                transaction.order_speaking.save()
            if transaction.order_writing is not None:
                transaction.order_writing.is_paid = True
                transaction.order_writing.save()
            return render(request, 'tpousers/transaction_result.html', {'transaction_status': True})
        else:
            return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})

    else:
        return render(request, 'tpousers/transaction_result.html', {'transaction_status': False})
