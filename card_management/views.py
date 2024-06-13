from rest_framework import viewsets
from .models import Card, CardDriverHistory
from .serializers import CardReadSerializer, CardWriteSerializer, CardDriverHistorySerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminRole
from rest_framework import generics
from users.permissions import IsAdminRole, IsStaffRole


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    permission_classes = [IsStaffRole]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CardWriteSerializer
        return CardReadSerializer
    
    def get_queryset(self):
        user = self.request.user
        if self.action in ['list', 'retrieve'] and user.role.lower() == "client":
            return Card.objects.filter(company=user.company)
        return Card.objects.all()

class CardDriverHistoryListView(generics.ListAPIView):
    serializer_class = CardDriverHistorySerializer
    queryset = CardDriverHistory.objects.all()
    permission_classes = [IsAuthenticated, IsStaffRole]

    def get_queryset(self):
        return CardDriverHistory.objects.all().order_by('end_date')

class ActiveCardsListView(generics.ListAPIView):
    serializer_class = CardReadSerializer
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated, IsStaffRole]

    def get_queryset(self):
        return Card.objects.filter(active=True)
