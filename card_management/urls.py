from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CardViewSet, CardDriverHistoryListView,
    ActiveCardsListView
)

router = DefaultRouter()
router.register(r'card', CardViewSet, basename='card')


urlpatterns = [
    path('', include(router.urls)),
    path('card/driver/history/', CardDriverHistoryListView.as_view()),
    path('card/active/list/', ActiveCardsListView.as_view()),
]