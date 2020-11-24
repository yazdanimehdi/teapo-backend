import os
import re

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from tpousers.models import UserReadingAnswers, UserWritingAnswers, UserListeningAnswers, UserSpeakingAnswers, TestUser, UserWritingCorrectionOrder, UserSpeakingCorrectionOrder
from tpo.models import ListeningQuestions, ReadingQuestions, Writing, Speaking
from institutions.models import Users
from django.core.files import File
import base64


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
def submit_listening_answer(request):
    test_id = request.data[1]
    try:
        user_test = TestUser.objects.get(test__id=test_id, user=request.user)
        answers = request.data[0]
        for item in answers:
            user_listening_answer, created = UserListeningAnswers.objects.get_or_create(
                question=ListeningQuestions.objects.get(id=item),
                user_test=user_test,
            )

            user_listening_answer.answer = answers[item]
            user_listening_answer.save()

        return Response(status=status.HTTP_200_OK)
    except TestUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
def submit_writing_answer(request):
    test_id = request.data[1]
    try:
        user_test = TestUser.objects.get(test__id=test_id, user=request.user)
        answers = request.data[0]
        for item in answers:
            user_writing_answer, created = UserWritingAnswers.objects.get_or_create(
                question=Writing.objects.get(id=item),
                user_test=user_test,
            )
            user_writing_answer.answer = answers[item]
            user_writing_answer.save()

        return Response(status=status.HTTP_200_OK)
    except TestUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
def submit_reading_answer(request):
    test_id = request.data[1]
    try:
        user_test = TestUser.objects.get(test__id=test_id, user=request.user)
        answers = request.data[0]
        for item in answers:
            user_reading_answer, created = UserReadingAnswers.objects.get_or_create(
                question=ReadingQuestions.objects.get(id=item),
                user_test=user_test,
            )
            user_reading_answer.answer = answers[item]
            user_reading_answer.save()

        return Response(status=status.HTTP_200_OK)
    except TestUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
def submit_speaking_answer(request):
    test_id = request.data[1]
    try:
        user_test = TestUser.objects.get(test__id=test_id, user=request.user)
        answers = request.data[0]
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
            # print(b)
            decoded = base64.decodebytes(b)

            speaking_file = open(f'{item}.webm', 'wb')
            speaking_file.write(decoded)
            speaking_file.close()
            file = open(f'{item}.webm', 'rb')
            djangofile = File(file)
            user_speaking_answer.answer = File(djangofile)
            user_speaking_answer.save()
            os.remove(f'{item}.webm')

        return Response(status=status.HTTP_200_OK)
    except TestUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
def submit_mock_done(request):
    user = request.user
    test_id = request.data['id']
    print(test_id)
    try:
        test_user = TestUser.objects.get(user=user, test__id=test_id)

    except TestUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    test_user.is_done = True
    test_user.reading_score = request.data['reading']
    test_user.listening_score = request.data['listening']
    if len(UserSpeakingAnswers.objects.filter(user_test=test_user)) != 0 or len(UserWritingAnswers.objects.filter(user_test=test_user)) != 0:
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

        if corrector_list.__len__() != 0:
            corrector_list.sort(key=lambda x: (-x[1], -x[2]))
            test_user.assigned_corrector = corrector_list[0][0]
        test_user.save()
        return Response(status=status.HTTP_200_OK)

    else:
        test_user.is_corrected = True
        test_user.save()
        return Response(status=status.HTTP_200_OK)