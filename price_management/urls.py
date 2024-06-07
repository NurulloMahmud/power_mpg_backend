from django.urls import path, include
from .views import (
    StoreViewSet, StorePriceViewSet,
    StorePriceByDate, StorePriceCreatePilotView,
    StorePriceCreateLovesView
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'store', StoreViewSet, basename='store')
router.register(r'storeprice', StorePriceViewSet, basename='storeprice')


urlpatterns = [
    path('', include(router.urls)),
    path('store-price-by-date/', StorePriceByDate.as_view()),
    path('store-price-create-pilot/', StorePriceCreatePilotView.as_view()),
    path('store-price-create-loves/', StorePriceCreateLovesView.as_view()),
]