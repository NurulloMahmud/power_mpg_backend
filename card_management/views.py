from rest_framework import viewsets
from .models import Card
from .serializers import CardReadSerializer, CardWriteSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminRole



class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CardWriteSerializer
        return CardReadSerializer
