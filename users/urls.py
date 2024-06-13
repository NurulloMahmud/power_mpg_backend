from django.urls import path, include
from .views import UserCreateView, UserListView, UserUpdateView, CompanyViewSet, CurrentUserView \
    , MyTokenObtainPairView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')


urlpatterns = [
    path('register/', UserCreateView.as_view()),
    path('list/', UserListView.as_view()),
    path('update/<int:pk>/', UserUpdateView.as_view()),
    path('current/', CurrentUserView.as_view()),
    path('', include(router.urls)),

    # simple jwt
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
