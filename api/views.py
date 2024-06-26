from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer
from users.models import UserCustom


class IsUserSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class UserListView(ListAPIView):
    queryset = UserCustom.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserSuperAdmin]


class UserCreateView(APIView):
    permission_classes = [IsAuthenticated, IsUserSuperAdmin]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(UpdateAPIView):
    queryset = UserCustom.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserSuperAdmin]


class UserDeleteView(DestroyAPIView):
    queryset = UserCustom.objects.all()
    permission_classes = [IsAuthenticated, IsUserSuperAdmin]
