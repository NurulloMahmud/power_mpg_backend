from django.urls import path, include
from .views import AccountTypeViewSet
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentListCreateView
)


router = DefaultRouter()
router.register(r'accounttype', AccountTypeViewSet, basename='accounttype')

urlpatterns = [
    path('', include(router.urls)),
    path('payment/', PaymentListCreateView.as_view()),
]