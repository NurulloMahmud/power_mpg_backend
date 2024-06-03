from django.urls import path
from .views import UserCreateView, UserListView, UserUpdateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', UserCreateView.as_view()),
    path('list/', UserListView.as_view()),
    path('update/<int:pk>/', UserUpdateView.as_view()),

    # simple jwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
