from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from decimal import Decimal
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, ExchangeRequestSerializer


# Create your views here.


def perform_exchange(user, amount):
        rate = Decimal('117.50')
        try :
            with transaction.atomic():
                source = Wallet.objects.select_for_update().get(user=user, currency='USD')
                if source.balance < amount:
                    return {"error": "Insufficient USD","status": status.HTTP_400_BAD_REQUEST}
                
                dest, _ = Wallet.objects.get_or_create(user=user, currency='BDT')
                source.balance -= amount
                dest.balance += (amount * rate)
                source.save()
                dest.save()
                
                Transaction.objects.create(wallet=source, tx_type='EXCHANGE', amount=-amount, balance_after=source.balance)
                Transaction.objects.create(wallet=dest, tx_type='EXCHANGE', amount=(amount*rate), balance_after=dest.balance)
                return {"message": "Exchange Successful","status": status.HTTP_200_OK}
        except Wallet.DoesNotExist:
            return {"error": "You don't have a USD wallet.", "status": status.HTTP_404_NOT_FOUND}


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
    


class ExchangeAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = ExchangeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        result = perform_exchange(request.user, amount)
        return Response(result, status=result.get('status'))

    # def perform_exchange(self, user, amount):
    #     rate = Decimal('117.50')
    #     with transaction.atomic():
    #         source = Wallet.objects.select_for_update().get(user=user, currency='USD')
    #         if source.balance < amount:
    #             return {"error": "Insufficient USD"}
            
    #         dest, _ = Wallet.objects.get_or_create(user=user, currency='BDT')
    #         source.balance -= amount
    #         dest.balance += (amount * rate)
    #         source.save()
    #         dest.save()
            
    #         Transaction.objects.create(wallet=source, tx_type='EXCHANGE', amount=-amount, balance_after=source.balance)
    #         Transaction.objects.create(wallet=dest, tx_type='EXCHANGE', amount=(amount*rate), balance_after=dest.balance)
    #         return {"message": "Exchange Successful (APIView)"}



class ExchangeGenericView(generics.CreateAPIView):
    serializer_class = ExchangeRequestSerializer
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = perform_exchange(request.user, serializer.validated_data['amount'])
        return Response(result, status=result.get('status'))

class ExchangeViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]

    @action(detail=False, methods=['post'])
    def do_exchange(self, request):
        serializer = ExchangeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = perform_exchange(request.user, serializer.validated_data['amount'])
        return Response(result, status=result.get('status'))
