from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from institutions.models import Users
from institutions.api.serializers import UserSerializer


class IsInstitute(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 4)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 5)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,  )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ObtainAPIToken(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            return Response(data=token[0].key, status=status.HTTP_200_OK)
        else:
            return Response(data=False, status=status.HTTP_200_OK)
