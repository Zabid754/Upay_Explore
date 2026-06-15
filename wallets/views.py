from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from decimal import Decimal
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, ExchangeRequestSerializer
from django.contrib.auth.models import User

# Create your views here.



def perform_exchange(sender, receiver_username, from_curr, to_curr, amount):
    amount = Decimal(str(amount))
    
    USD_TO_BDT_RATE = Decimal('117.50')
    BDT_TO_USD_RATE = Decimal('0.0085') 
    
    if from_curr == to_curr:
        rate = Decimal('1.0') 
    elif from_curr == 'USD' and to_curr == 'BDT':
        rate = USD_TO_BDT_RATE
    elif from_curr == 'BDT' and to_curr == 'USD':
        rate = BDT_TO_USD_RATE
    else:
        return {"error": "Invalid currency pair", "status": 400}

    try:
        receiver = User.objects.get(username=receiver_username)

        with transaction.atomic():
            source_wallet = Wallet.objects.select_for_update().get(user=sender, currency=from_curr)
            current_source_balance = Decimal(str(source_wallet.balance))
            
            if current_source_balance < amount:
                return {"error": f"Insufficient {from_curr} balance", "status": 400}

            dest_wallet, _ = Wallet.objects.get_or_create(user=receiver, currency=to_curr)
            current_dest_balance = Decimal(str(dest_wallet.balance))

            converted_amount = amount * rate

            source_wallet.balance = current_source_balance - amount
            dest_wallet.balance = current_dest_balance + converted_amount

            source_wallet.save()
            dest_wallet.save()

            is_internal = (sender == receiver)
            
            Transaction.objects.create(
                wallet=source_wallet, 
                tx_type='EXCHANGE' if is_internal else 'WITHDRAW', 
                amount=-amount, 
                balance_after=source_wallet.balance,
            )
            
            Transaction.objects.create(
                wallet=dest_wallet, 
                tx_type='EXCHANGE' if is_internal else 'DEPOSIT', 
                amount=converted_amount, 
                balance_after=dest_wallet.balance,
            )

            return {
                "message": "Transaction Successful",
                "sent": f"{amount} {from_curr}",
                "received": f"{converted_amount} {to_curr}",
                "status": 200
            }

    except User.DoesNotExist:
        return {"error": "Receiver user not found", "status": 404}
    except Wallet.DoesNotExist:
        return {"error": f"You do not have a {from_curr} wallet", "status": 404}



# def perform_exchange(user, amount):
#         rate = Decimal('117.50')
#         try :
#             with transaction.atomic():
#                 source = Wallet.objects.select_for_update().get(user=user, currency='USD')
#                 if source.balance < amount:
#                     return {"error": "Insufficient USD","status": status.HTTP_400_BAD_REQUEST}
                
#                 dest, _ = Wallet.objects.get_or_create(user=user, currency='BDT')
#                 source.balance -= amount
#                 dest.balance += (amount * rate)
#                 source.save()
#                 dest.save()
                
#                 Transaction.objects.create(wallet=source, tx_type='EXCHANGE', amount=-amount, balance_after=source.balance)
#                 Transaction.objects.create(wallet=dest, tx_type='EXCHANGE', amount=(amount*rate), balance_after=dest.balance)
#                 return {"message": "Exchange Successful","status": status.HTTP_200_OK}
#         except Wallet.DoesNotExist:
#             return {"error": "You don't have a USD wallet.", "status": status.HTTP_404_NOT_FOUND}


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
        #amount = serializer.validated_data['amount']
        #result = perform_exchange(request.user, amount)
        #return Response(result, status=result.get('status'))
        result = perform_exchange(
            sender=request.user, 
            receiver_username=serializer.validated_data['receiver_username'],
            from_curr=serializer.validated_data['from_currency'],
            to_curr=serializer.validated_data['to_currency'],
            amount=serializer.validated_data['amount']
        )
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
        # result = perform_exchange(request.user, serializer.validated_data['amount'])
        # return Response(result, status=result.get('status'))
        result = perform_exchange(
            sender=request.user, 
            receiver_username=serializer.validated_data['receiver_username'],
            from_curr=serializer.validated_data['from_currency'],
            to_curr=serializer.validated_data['to_currency'],
            amount=serializer.validated_data['amount']
        )
        return Response(result, status=result.get('status'))

class ExchangeViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]

    @action(detail=False, methods=['post'])
    def do_exchange(self, request):
        serializer = ExchangeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # result = perform_exchange(request.user, serializer.validated_data['amount'])
        # return Response(result, status=result.get('status'))
        result = perform_exchange(
            sender=request.user, 
            receiver_username=serializer.validated_data['receiver_username'],
            from_curr=serializer.validated_data['from_currency'],
            to_curr=serializer.validated_data['to_currency'],
            amount=serializer.validated_data['amount']
        )
        return Response(result, status=result.get('status'))



class WalletListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def delete(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    