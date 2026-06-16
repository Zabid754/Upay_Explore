from rest_framework import serializers
from .models import Wallet, Transaction
from django.contrib.auth.models import User
from decimal import Decimal

class MoneyField(serializers.ReadOnlyField):
    def to_representation(self, value):
        rate = Decimal('117.50')
        return f"BDT {value * rate}"

class MaskedUserField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return f"{value[0]}{'*' * (len(value)-2)}{value[-1]}"
    
class MaskedCardField(serializers.ReadOnlyField):
    """Task 3: Custom Field - Masks sensitive info except last 4."""
    def to_representation(self, value):
        if not value: return ""
        str_val = str(value)
        return f"****-****-{str_val[-4:]}"
    


    
class UserSerializer(serializers.ModelSerializer):
    username = MaskedUserField() 

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    transaction_count = serializers.SerializerMethodField()
    balance_in_taka = MoneyField(source='balance')
    account_number_masked = MaskedCardField(source='id')

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'currency', 'balance', 'balance_in_taka', 'account_number_masked', 'transaction_count', 'is_frozen', 'created_at']
        read_only_fields = ['balance'] 
    
    def get_transaction_count(self, obj):
        return obj.transactions.count()
    
class TransactionListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return super().to_representation(data)

class TransactionSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only = True)
    class Meta:
        model = Transaction
        list_serializer_class = TransactionListSerializer
        #fields = '__all__'
        fields = ['id', 'wallet', 'tx_type', 'amount', 'balance_after', 'timestamp']

    def validate_amount(self, value):
        if value == 0:
            raise serializers.ValidationError("Amount cannot be zero.")
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_large_transaction'] = abs(instance.amount) > 1000
        return representation
    

class ExchangeRequestSerializer(serializers.Serializer):
    receiver_username = serializers.CharField()
    from_currency = serializers.ChoiceField(choices=['USD', 'BDT'])
    to_currency = serializers.ChoiceField(choices=['USD', 'BDT'])
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

    def validate(self, data):
        if data['from_currency'] == data['to_currency']:
            raise serializers.ValidationError("Source and target currencies must be different.")
        return data

class WalletListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'currency', 'balance']

class TransactionCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    currency = serializers.ChoiceField(choices=['USD', 'BDT'], write_only=True)

    class Meta:
        model = Transaction
        fields = ['username', 'currency', 'tx_type', 'amount']

    def create(self, validated_data):
        username = validated_data.pop('username')
        currency = validated_data.pop('currency')
        
        user = User.objects.get(username=username)
        wallet, _ = Wallet.objects.get_or_create(user=user, currency=currency)
        
        return Transaction.objects.create(wallet=wallet, **validated_data, balance_after=wallet.balance)
    

