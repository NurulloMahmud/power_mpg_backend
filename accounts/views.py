from rest_framework.viewsets import ModelViewSet
from .models import AccountType
from .serializers import AccountTypeSerializer



class AccountTypeViewSet(ModelViewSet):
    from users.permissions import IsAdminRole
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAdminRole]
