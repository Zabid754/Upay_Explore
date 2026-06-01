from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, CheckConstraint


# 1. Custom Manager to filter active accounts only
class ActiveAccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='active')

# 2. Account Model
class Account(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('frozen', 'Frozen')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    objects = models.Manager() # Default
    active_accounts = ActiveAccountManager() # Custom

    class Meta:
        indexes = [models.Index(fields=['account_number', 'status'])]
        constraints = [
            # FIXED: Changed 'check' to 'condition' for Django 5.0/6.0 compatibility
            CheckConstraint(
                condition=Q(balance__gte=0), 
                name="balance_not_negative",
                violation_error_message="Transaction failed: Account balance cannot go below zero."
            )
        ]

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"

# 3. Merchant Model
class Merchant(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    trust_score = models.IntegerField(default=100)

    def __str__(self):
        return self.name

# 4. Transaction Model
class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_tx')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_tx')
    merchant = models.ForeignKey(Merchant, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=['timestamp'])]

# 5. Card Model
class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Card {self.card_number} ({self.account.user.username})"