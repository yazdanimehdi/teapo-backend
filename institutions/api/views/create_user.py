from rest_framework import generics
from rest_framework.permissions import AllowAny, BasePermission
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
    permission_classes = (AllowAny, )

