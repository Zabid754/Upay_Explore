from django.db.models import F, Q, Sum, Avg, Count, Max, Min, Case, When, Value, CharField
from django.contrib.auth.models import User
from fintech_payment.models import Account, Transaction, Merchant

# 1. Using Q objects for OR logic (Transactions > 1000 OR sender is 'admin')
q1 = Transaction.objects.filter(Q(amount__gt=1000) | Q(sender__user__username='admin'))

# 2. Using F expression to prevent race conditions (Subtracting fee atomically)
# Account.objects.filter(id=1).update(balance=F('balance') - 10)

# 3. select_related for optimization (Joins Transaction, Account, and User in 1 SQL query)
q3 = Transaction.objects.select_related('sender__user').all()

# 4. Annotation: Calculate total money sent by each account
q4 = Account.objects.annotate(total_spent=Sum('sent_tx__amount'))

# 5. prefetch_related: Fetch all users and their related accounts efficiently (2 queries)
q5 = User.objects.prefetch_related('accounts').all()

# 6. Aggregation: Find the average transaction amount across the whole app
q6 = Transaction.objects.aggregate(avg_amount=Avg('amount'))

# 7. Filtering on Annotation: Find users who have more than 2 accounts
q7 = User.objects.annotate(acc_count=Count('accounts')).filter(acc_count__gt=2)

# 8. Conditional Expression (Case/When): Label accounts as 'VIP' if balance > 5000
q8 = Account.objects.annotate(
    user_tier=Case(
        When(balance__gt=5000, then=Value('VIP')),
        When(balance__gt=1000, then=Value('Regular')),
        default=Value('Basic'),
        output_field=CharField(),
    )
)

# 9. F() expression: Find transactions where the amount is greater than the sender's current balance (shouldn't happen)
q9 = Transaction.objects.filter(amount__gt=F('sender__balance'))

# 10. Max Aggregation: Find the most expensive transaction for each merchant
q10 = Merchant.objects.annotate(largest_tx=Max('transaction__amount'))

# 11. Subquery-like: Find accounts with balance higher than the global average
avg_bal = Account.objects.aggregate(Avg('balance'))['balance__avg'] or 0
q11 = Account.objects.filter(balance__gt=avg_bal)

# 12. Using .values() and .annotate(): Sum of transactions per merchant category
q12 = Merchant.objects.values('category').annotate(total_sales=Sum('transaction__amount'))

# 13. Complex Filter: Merchants who have had transactions from users with 'gmail' emails
q13 = Merchant.objects.filter(transaction__sender__user__email__contains='gmail').distinct()

# 14. Annotation with Filter: Total successful (sent) transactions excluding merchant payments
q14 = Account.objects.annotate(p2p_sent=Sum('sent_tx__amount', filter=Q(sent_tx__merchant__isnull=True)))

# 15. Optimization comparison (N+1 demonstration)
# SLOW:
slow = [tx.sender.user.username for tx in Transaction.objects.all()]
# FAST:
fast = Transaction.objects.select_related('sender__user')