from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpo.models import TestReading, Reading, ReadingQuestions, ReadingAnswers
from tpo.api.serializers import ReadingQuestionSerializer
from rest_framework import status


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_reading_list(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            readings = Reading.objects.filter(Q(institute=user) | Q(institute=user.institute)).order_by('id')
            reading_list = []
            for reading in readings:
                reading_obj = {}
                tests = []
                for item in TestReading.objects.filter(reading=reading):
                    tests.append(item.test.title)
                reading_obj['title'] = reading.title
                reading_obj['passage'] = reading.passage
                reading_obj['tests'] = tests
                reading_obj['id'] = reading.id
                reading_list.append(reading_obj)
            return Response(data=reading_list, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def add_reading(request):
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
                reading_passage += f'<p id="{i}">' + item + '</p>'
                i += 1
            reading.passage = reading_passage
            if user.role == 4:
                reading.institute = user
            else:
                reading.institute = user.institute
            reading.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def delete_reading(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            reading = Reading.objects.get(Q(id=request.data['id']) & (Q(institute=user) | Q(institute=user.institute)))
            reading.delete()
            Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Reading.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def edit_reading(request):
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
            Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Reading.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_reading_questions(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            reading = Reading.objects.get(
                Q(id=request.GET.get('id')) & (Q(institute=user) | Q(institute=user.institute)))
            return Response(
                data=[ReadingQuestionSerializer(q).data for q in
                      ReadingQuestions.objects.filter(reading=reading).order_by('-number')],
                status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Reading.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def delete_reading_question(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            question = ReadingQuestions.objects.get(
                Q(id=request.data['id']) & (Q(reading__institute=user) | Q(reading__institute=user.institute)))
            question.delete()
            return Response(status=status.HTTP_200_OK)
        except ReadingQuestions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def add_reading_question(request):
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
            question.right_answer = request.data['right_answer']

            if question.question_type == 'Insertion':
                question.insertion_sentence = request.data['insertion_sentence']

            question.save()
            if question.question_type != 'Insertion':
                for index, choice in enumerate(request.data['answers']):
                    answer = ReadingAnswers()
                    answer.question = question
                    answer.answer = choice
                    answer.code = index + 1
                    answer.save()

            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Reading.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)