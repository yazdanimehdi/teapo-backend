from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tpo.api.serializers import TestSerializer, MockListSerializer, AssignmentListSerializer, TPOListSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpo.models import Test
from tpousers.models import TestUser
from rest_framework import status


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def test_download_api_view(request):
    test_id = request.GET.get('id')
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    is_paid = False
    user_tests = TestUser.objects.filter(test=test)
    for user_test in user_tests:
        if user_test.is_paid is True:
            is_paid = True

    if test.mode == 'T' or is_paid is True or (test.mode == 'A' and request.user in test.class_assigned.students.all()):
        return Response(data=TestSerializer(test).data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_tpo_list(request):
    tpo_test = Test.objects.filter(Q(mode='T') | Q(mode='P'))
    return Response([TPOListSerializer(x).data for x in tpo_test], status=status.HTTP_200_OK)

