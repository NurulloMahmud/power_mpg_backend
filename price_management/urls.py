from django.urls import path, include
from .views import (
    StoreViewSet, StorePriceViewSet,
    StorePriceByDate
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'store', StoreViewSet, basename='store')
router.register(r'storeprice', StorePriceViewSet, basename='storeprice')


urlpatterns = [
    path('', include(router.urls)),
    path('store-price-by-date/', StorePriceByDate.as_view()),
]