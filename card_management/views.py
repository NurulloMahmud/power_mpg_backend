from rest_framework import viewsets
from .models import Card, CardDriverHistory
from .serializers import CardReadSerializer, CardWriteSerializer, CardDriverHistorySerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminRole
from rest_framework import generics
from users.permissions import IsAdminRole, IsStaffRole


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CardWriteSerializer
        return CardReadSerializer

class CardDriverHistoryListView(generics.ListAPIView):
    serializer_class = CardDriverHistorySerializer
    queryset = CardDriverHistory.objects.all()
    permission_classes = [IsAuthenticated, IsStaffRole]

    def get_queryset(self):
        return CardDriverHistory.objects.all().order_by('end_date')

