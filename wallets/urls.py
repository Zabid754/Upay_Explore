from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionHistoryAPIView, TransactionHistoryGeneric, TransactionViewSet

router = DefaultRouter()
router.register(r'history-viewset', TransactionViewSet, basename='transaction-history')

urlpatterns = [
    path('history-api/', TransactionHistoryAPIView.as_view(), name='history-api'),
    path('history-generic/', TransactionHistoryGeneric.as_view(), name='history-generic'),
    path('', include(router.urls)),
]

