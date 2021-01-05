from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from tpo.models import TestSpeaking, Speaking
from rest_framework import status


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_speaking_list(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            speakings = Speaking.objects.filter(Q(institute=user) | Q(institute=user.institute)).order_by('id')
            speakings_list = []
            for speaking in speakings:
                speaking_obj = {}
                tests = []
                for item in TestSpeaking.objects.filter(speaking=speaking):
                    tests.append(item.test.title)
                speaking_obj['id'] = speaking.id
                speaking_obj['number'] = speaking.number
                speaking_obj['speaking_reading'] = speaking.speaking_reading
                speaking_obj['speaking_question'] = speaking.speaking_question
                if speaking.speaking_audio_file:
                    speaking_obj['speaking_audio_file'] = speaking.speaking_audio_file.url

                speaking_obj['tests'] = tests

                speakings_list.append(speaking_obj)
            return Response(data=speakings_list, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def delete_speaking(request):
    user = request.user
    if user.role == 4 or user.role == 2:
        try:
            speaking = Speaking.objects.get(Q(id=request.data['id']) & (Q(institute=user) | Q(institute=user.institute)))
            speaking.delete()
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Speaking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
