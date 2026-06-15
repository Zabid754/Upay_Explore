from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionHistoryAPIView, TransactionHistoryGeneric, TransactionViewSet, ExchangeAPIView, ExchangeGenericView, ExchangeViewSet, WalletListCreateAPIView, WalletDetailAPIView, WalletStatementAPIView, WalletViewSet

router = DefaultRouter()
router.register(r'history-viewset', TransactionViewSet, basename='transaction-history')
router.register(r'exchange-viewset', ExchangeViewSet, basename='exchange-viewset')
router.register(r'wallets-v4', WalletViewSet, basename='wallets-v4')

urlpatterns = [
    path('history-api/', TransactionHistoryAPIView.as_view(), name='history-api'),
    path('history-generic/', TransactionHistoryGeneric.as_view(), name='history-generic'),
    path('exchange-api/', ExchangeAPIView.as_view(), name='exchange-api'),
    path('exchange-generic/', ExchangeGenericView.as_view(), name='exchange-generic'),
    path('accounts/', WalletListCreateAPIView.as_view(), name='wallet-list'),
    path('accounts/<int:pk>/', WalletDetailAPIView.as_view(), name='wallet-detail'),
    path('accounts/<int:pk>/statement/', WalletStatementAPIView.as_view(), name='wallet-statement'),
    path('', include(router.urls)),
]

