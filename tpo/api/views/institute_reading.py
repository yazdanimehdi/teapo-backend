from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpo.api.serializers.reading import ReadingQuestionSerializer
from tpo.models import ReadingQuestions, TestReading, Reading, ReadingAnswers
from rest_framework import status
import re
from datetime import datetime


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_institute_reading(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        reading_list = []
        readings = Reading.objects.filter(institute=user)

        for reading in readings:
            reading_obj = {}
            tests_list = []
            tests = TestReading.objects.filter(reading=reading)
            for test in tests:
                tests_list.append(test.test.title)
            reading_obj['id'] = reading.id
            reading_obj['tests'] = tests_list
            reading_obj['title'] = reading.title
            passage = re.sub(r'\r\n', ' ', reading.passage)
            reading_obj['passage'] = passage

            reading_list.append(reading_obj)
        return Response(data=reading_list, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def add_institute_reading(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            reading = Reading()
            reading.title = request.data['title']
            passage = request.data['passage']
            passage_paragraph_list = passage.split('\n')
            reading_passage = ''
            i = 1
            for item in passage_paragraph_list:
                reading_passage += f'<pr id="{i}">' + item + '</p>'
                i += 1
            reading.passage = reading_passage
            reading.institute = user
            reading.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def delete_institute_reading(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            reading = Reading.objects.get(Q(id=request.data['id']) & (Q(institute=user) | Q(institute=user.institute)))
            reading.delete()
            return Response(status=status.HTTP_200_OK)
        except Reading.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def edit_institute_reading(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            reading = Reading.objects.get(Q(id=request.data['id']) & (Q(institute=user) | Q(institute=user.institute)))
            reading.title = request.data['title']
            passage = request.data['passage']
            passage_paragraph_list = passage.split('\n')
            reading_passage = ''
            i = 1
            for item in passage_paragraph_list:
                reading_passage += f'<p id="{i}">' + item + '</p>'
                i += 1
            reading.passage = reading_passage
            reading.save()
            return Response(status=status.HTTP_200_OK)
        except Reading.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_institute_reading_questions(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        question_list = [ReadingQuestionSerializer(x).data for x in
                         ReadingQuestions.objects.filter(reading__id=request.GET.get('id'))]
        question_list.sort(key=lambda x: -x['number'])
        return Response(data=question_list, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def delete_institute_reading_question(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            question = ReadingQuestions.objects.get(id=request.data['id'])
            question.delete()
            return Response(status=status.HTTP_200_OK)
        except ReadingQuestions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def add_institute_reading_question(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            reading = Reading.objects.get(Q(id=request.data['reading_id']) & (Q(institute=user) | Q(institute=user.institute)))
            question = ReadingQuestions()
            question.reading = reading
            question.question = request.data['question']
            question.question_type = request.data['question_type']
            question.number = request.data['number']
            question.related_paragraph = request.data['related_paragraph']
            question.related_passage = request.data['related_passage']
            question.related_passage_title = reading.title
            question.right_answer = request.data['right_answer'].strip()
            if question.question_type == 'Insertion':
                question.insertion_sentence = request.data['insertion_sentence']

            question.save()

            if question.question_type != 'Insertion':
                for idx, answers in enumerate(request.data['answers']):
                    answer = ReadingAnswers()
                    answer.question = question
                    answer.answer = answers
                    answer.code = idx + 1
                    answer.save()

            return Response(status=status.HTTP_200_OK)
        except Reading.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)