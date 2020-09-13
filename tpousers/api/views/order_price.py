from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpousers.models import GlobalVariables, UserWritingCorrectionOrder, UserSpeakingCorrectionOrder
from rest_framework import status
from tpousers.api.serializers import UserSpeakingCorrectionOrderSerializer, UserWritingCorrectionOrderSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def correction_price(request):
    price_speaking = GlobalVariables.objects.get(key='SpeakingPrice').value
    price_writing = GlobalVariables.objects.get(key='WritingPrice').value
    correction_writing_order_list = UserWritingCorrectionOrder.objects.filter(user=request.user, is_paid=True)
    writing_list = [UserWritingCorrectionOrderSerializer(x).data for x in correction_writing_order_list]
    correction_speaking_order_list = UserSpeakingCorrectionOrder.objects.filter(user=request.user, is_paid=True)
    speaking_list = [UserSpeakingCorrectionOrderSerializer(x).data for x in correction_speaking_order_list]

    return Response(data={'speaking_price': int(price_speaking), 'writing_price': int(price_writing),
                          'writing_list': writing_list, 'speaking_list': speaking_list},
                    status=status.HTTP_200_OK)
