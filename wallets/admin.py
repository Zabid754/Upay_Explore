from django.contrib import admin
from .models import Wallet, Transaction

# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user','balance','currency','is_frozen')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet','tx_type','amount','balance_after','timestamp')