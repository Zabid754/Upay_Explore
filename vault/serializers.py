from rest_framework import serializers
from .models import Account, Transaction

# Serializer for Transaction model
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

# Serializer 1: Basic View (used for the "List" view)
# Task 4: Only show essential info in the list
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'balance', 'is_frozen']

# Serializer 2: Detailed View (used for the "Retrieve/Detail" view)
# Task 4: Show full details, including the owner's username
class AccountDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'balance', 'is_frozen', 'owner_username']
        read_only_fields = ['balance'] # Safety: prevent balance editing via API