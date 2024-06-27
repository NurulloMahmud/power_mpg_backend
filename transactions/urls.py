from django.urls import path
from .views import (
    TransactionCreateView, TransactionListView,
    TransactionAmountSummaryView
)



urlpatterns = [
    path('create/', TransactionCreateView.as_view()),
    path('list/', TransactionListView.as_view()),
    path('amount-summary/', TransactionAmountSummaryView.as_view()),
]