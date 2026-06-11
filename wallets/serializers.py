from rest_framework import serializers
from .models import Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'currency', 'balance', 'is_frozen', 'created_at']
        read_only_fields = ['balance'] 

class TransactionSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only = True)
    class Meta:
        model = Transaction
        #fields = '__all__'
        fields = ['id', 'wallet', 'tx_type', 'amount', 'balance_after', 'timestamp']

class ExchangeRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)