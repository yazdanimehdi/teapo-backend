from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpousers.models import GlobalVariables
from rest_framework import status


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def order_speaking_correction(request):
    price = GlobalVariables.objects.get(key='SpeakingPrice').value
    return Response(data=int(price), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def order_writing_correction(request):
    price = GlobalVariables.objects.get(key='WritingPrice').value
    return Response(data=int(price), status=status.HTTP_200_OK)
