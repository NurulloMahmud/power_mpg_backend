from rest_framework import viewsets, generics
from .serializers import StoreSerializer, StorePriceReadSerializer, StorePriceWriteSerializer
from .models import Store, StorePrice
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminRole, IsStaffRole


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticated, IsStaffRole]

class StorePriceViewSet(viewsets.ModelViewSet):
    queryset = StorePrice.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StorePriceWriteSerializer
        return StorePriceReadSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAdminRole()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return StorePrice.objects.all().order_by('-date')

class StorePriceByDate(generics.ListAPIView):
    serializer_class = StorePriceReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date = self.request.query_params.get('date')
        return StorePrice.objects.filter(date=date)
