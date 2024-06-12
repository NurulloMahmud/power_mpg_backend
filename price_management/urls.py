from django.urls import path, include
from .views import (
    StoreViewSet, StorePriceViewSet,
    StorePriceByDate, StorePriceCreatePilotView,
    StorePriceCreateLovesView, StorePriceCheckView,
    StorePriceDeleteView
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'store', StoreViewSet, basename='store')
router.register(r'storeprice', StorePriceViewSet, basename='storeprice')


urlpatterns = [
    path('', include(router.urls)),
    path('store-price-by-date/', StorePriceByDate.as_view()),
    path('store-price-create-pilot/', StorePriceCreatePilotView.as_view()),
    path('store-price-check/<str:date>/<str:store_name>/', StorePriceCheckView.as_view()),
    path('store-price-delete/<str:date>/<str:store_name>/', StorePriceDeleteView.as_view()),
    path('store-price-create-loves/', StorePriceCreateLovesView.as_view()), # add later
]