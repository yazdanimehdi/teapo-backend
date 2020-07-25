from rest_framework.permissions import AllowAny

from tpo.api.serializers import ListeningSerializer
from tpo.models import Listening
from rest_framework import generics


class TestDownloadAPIView(generics.ListAPIView):
    queryset = Listening.objects.filter(id=2)
    serializer_class = ListeningSerializer
    permission_classes = (AllowAny,)