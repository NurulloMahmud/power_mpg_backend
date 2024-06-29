from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import AccountType, Payment
from .serializers import AccountTypeSerializer, PaymentReadSerializer, PaymentWriteSerializer



class AccountTypeViewSet(ModelViewSet):
    from users.permissions import IsAdminRole
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAdminRole]

class PaymentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(account__company=self.request.user.company)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PaymentReadSerializer
        return PaymentWriteSerializer
