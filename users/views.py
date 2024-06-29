from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser, Company, CompanyStatus
from .serializers import (
    UserRegisterSerializer, UserListSerializer,
    UserUpdateSerializer, CompanySerializer,
    CurrentUserSerializer, MyTokenObtainPairSerializer,
    CompanyWriteSerializer, CompanyStatusSerializer
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
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CompanyWriteSerializer
        return CompanySerializer
    
    def create(self, request, *args, **kwargs):
        from accounts.models import Account

        data = request.data
        account_type = data.pop('account_type', None)
        if not account_type:
            raise ValueError('Account type is required')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        account = Account.objects.create(
            company=company,
            account_type=account_type
        )
        
        account.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class CurrentUserView(APIView):
    def get(self, request):
        user = request.user
        serializer = CurrentUserSerializer(user)
        return Response(serializer.data)

class CompanyStatusViewset(ModelViewSet):
    queryset = CompanyStatus.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = CompanyStatusSerializer

#   customizing simple jwt to return user's role
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
