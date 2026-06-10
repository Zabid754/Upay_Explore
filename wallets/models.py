from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wallet(models.Model):
    CURRENCY_CHOICES = [('USD', 'USD'), ('BDT', 'BDT')]
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    is_frozen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'currency') 

    def __str__(self):
        return f"{self.user.username} - {self.balance} {self.currency}"

class Transaction(models.Model):
    TX_TYPES = [('EXCHANGE', 'Currency Exchange'), ('DEPOSIT', 'Deposit'), ('WITHDRAW', 'Withdraw')]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    tx_type = models.CharField(max_length=20, choices=TX_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tx_type} of {self.amount} by {self.wallet.user.username}"