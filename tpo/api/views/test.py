from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tpo.api.serializers import TestSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpo.models import Test, TestReading, TestListening, TestSpeaking, TestWriting
from tpousers.models import TestUser, UserTestOwnership
from rest_framework import status

from datetime import datetime


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
    my_list = []
    for item in tpo_test:
        tpo_test_dict = {'id': item.id, 'title': item.title, 'code': item.code, 'mode': item.mode,
                         'paid': UserTestOwnership.objects.filter(test=item, user=request.user,
                                                                  is_paid=True).__len__() != 0}
        my_list.append(tpo_test_dict)

    return Response(my_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_mock_list(request):
    mock_test = Test.objects.filter(
        Q(mode='M') & Q(start_time__lte=datetime.now()) & Q(end_time__gte=datetime.now()) & (~Q(
            testuser__user=request.user) | (Q(testuser__user=request.user) & Q(testuser__is_done=False))))
    mock_list = []

    for item in mock_test:
        try:
            test_user = TestUser.objects.get(test__id=item.id)
            is_paid = test_user.is_paid
        except TestUser.DoesNotExist:
            is_paid = None
        mock_test_dict = {
            'id': item.id,
            'title': item.title,
            'code': item.code,
            'reading': [x.reading.title for x in TestReading.objects.filter(test__id=item.id)],
            'listening': [x.listening.title for x in TestListening.objects.filter(test__id=item.id)],
            'speaking': [x.speaking.related for x in TestSpeaking.objects.filter(test__id=item.id)],
            'writing': [x.writing.related for x in TestWriting.objects.filter(test__id=item.id)],
            'institute': item.institute.name,
            'end_date': int(item.end_time.timestamp() * 1000),
            'is_paid': is_paid,
            'fee': item.fee
        }
        mock_list.append(mock_test_dict)
    return Response(mock_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_user_mock_list(request):
    user = request.user
    user_mock_test = TestUser.objects.filter(user=user, test__mode='M', is_done=True)
    user_mock_list = []
    for item in user_mock_test:
        mock_test_dict = {
            'id': item.id,
            'title': item.test.title,
            'code': item.test.code,
            'institute': item.test.institute.name,
            'date': int(item.date_time.timestamp() * 1000),
            'reading_score': item.reading_score,
            'listening_score': item.listening_score,
            'speaking_score': item.speaking_score,
            'writing_score': item.writing_score,
            'fee': item.fee
        }
        user_mock_list.append(mock_test_dict)
    return Response(user_mock_list, status=status.HTTP_200_OK)
