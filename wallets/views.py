from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from decimal import Decimal
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, ExchangeRequestSerializer


# Create your views here.


class TransactionHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        txs = Transaction.objects.filter(wallet__user=request.user)
        serializer = TransactionSerializer(txs, many=True)
        return Response(serializer.data)

class TransactionHistoryGeneric(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)


