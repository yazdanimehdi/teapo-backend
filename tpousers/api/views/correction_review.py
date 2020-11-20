from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpousers.models import UserWritingCorrectionOrder, UserSpeakingCorrectionOrder
from rest_framework import status
from tpousers.api.serializers import UserSpeakingCorrectionOrderSerializer, UserWritingCorrectionOrderSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def correction_review(request):
    order_type = request.GET.get('type')
    order_id = request.GET.get('id')
    if order_type == 'speaking':
        try:
            correction_model = UserSpeakingCorrectionOrder.objects.get(id=order_id)
        except UserSpeakingCorrectionOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK, data=UserSpeakingCorrectionOrderSerializer(correction_model).data)

    if order_type == 'writing':
        try:
            correction_model = UserWritingCorrectionOrder.objects.get(id=order_id)
        except UserWritingCorrectionOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK, data=UserWritingCorrectionOrderSerializer(correction_model).data)