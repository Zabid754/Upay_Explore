from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    # Link to user for Task 4 (Filtering by logged-in user)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Field to support Task 3 (Freeze action)
    is_frozen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"

class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Field to support Task 3 (Reverse action)
    is_reversed = models.BooleanField(default=False)

    def __str__(self):
        return f"Tx: {self.sender.account_number} -> {self.receiver.account_number} (${self.amount})"