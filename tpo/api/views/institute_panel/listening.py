from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpo.models import TestListening, Listening, ListeningQuestions, ListeningAnswers
from tpo.api.serializers import ListeningQuestionSerializer
from rest_framework import status
import json


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_listening_list(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            listening = Listening.objects.filter(Q(institute=user) | Q(institute=user.institute)).order_by('id')
            listening_list = []
            for l in listening:
                listening_obj = {}
                tests = []
                for item in TestListening.objects.filter(listening=l):
                    tests.append(item.test.title)
                listening_obj['listening'] = l.listening.url
                listening_obj['listening_image'] = l.listening_image.url
                listening_obj['type'] = l.type
                listening_obj['title'] = l.title
                listening_obj['transcript'] = l.transcript
                listening_obj['tests'] = tests
                listening_obj['id'] = l.id
                listening_list.append(listening_obj)
            return Response(data=listening_list, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def add_listening(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            listening = Listening()
            listening.listening = request.FILES['listening']
            listening.listening_image = request.FILES['listening_image']
            listening.type = request.data['type']
            listening.title = request.data['title']
            listening.transcript = request.data['transcript']

            if user.role == 4:
                listening.institute = user
            else:
                listening.institute = user.institute
            listening.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def delete_listening(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            listening = Listening.objects.get(Q(id=request.data['id']) & (Q(institute=user) | Q(institute=user.institute)))
            listening.delete()
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Listening.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def edit_listening(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            listening = Listening.objects.get(Q(id=request.data['id']) & (Q(institute=user) | Q(institute=user.institute)))
            if request.FILES['listening']:
                listening.listening = request.FILES['listening']
            if request.FILES['listening_image']:
                listening.listening_image = request.FILES['listening_image']
            listening.type = request.data['type']
            listening.title = request.data['title']
            listening.transcript = request.data['transcript']
            listening.save()
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Listening.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_listening_questions(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            listening = Listening.objects.get(
                Q(id=request.GET.get('id')) & (Q(institute=user) | Q(institute=user.institute)))
            return Response(
                data=[ListeningQuestionSerializer(q).data for q in
                      ListeningQuestions.objects.filter(listening=listening).order_by('-number')],
                status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Listening.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def delete_listening_question(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            question = ListeningQuestions.objects.get(
                Q(id=request.data['id']) & (Q(listening__institute=user) | Q(listening__institute=user.institute)))
            question.delete()
            return Response(status=status.HTTP_200_OK)
        except ListeningQuestions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def add_listening_question(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            listening = Listening.objects.get(
                Q(id=request.data['listening_id']) & (Q(institute=user) | Q(institute=user.institute)))
            question = ListeningQuestions()
            question.listening = listening
            question.question = request.data['question']
            question.number = request.data['number']
            question.listening_question_audio_file = request.FILES['listening_question_audio_file']
            if request.data['quote'] == 'false':
                question.quote = False
            if request.data['quote'] == 'true':
                question.quote = True

            question.right_answer = request.data['right_answer'].strip()

            if question.quote is True:
                question.quote_audio_file = request.FILES['quote_audio_file']

            question.save()
            for index, choice in enumerate(json.loads(request.data['answers'])):
                answer = ListeningAnswers()
                answer.question = question
                answer.answer = choice
                answer.code = index + 1
                answer.save()

            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Listening.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
