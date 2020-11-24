from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from institutions.models import News
import datetime


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
def get_news(request):
    news_inst = News.objects.filter(date_time__gte=(datetime.datetime.now() + datetime.timedelta(5))).order_by('-id')[:4]
    news = []
    for item in news_inst:
        news.append({'id': item.id, 'title': item.title, 'link': item.link})
    return Response(data=news, status=status.HTTP_200_OK)
