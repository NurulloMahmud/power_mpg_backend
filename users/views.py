from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import (
    UserRegisterSerializer, UserListSerializer,
    UserUpdateSerializer,
)
from .permissions import IsAdminRole



class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

