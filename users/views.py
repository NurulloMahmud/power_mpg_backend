from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Company
from .serializers import (
    UserRegisterSerializer, UserListSerializer,
    UserUpdateSerializer, CompanySerializer
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

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

