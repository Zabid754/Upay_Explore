from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from .models import Account, Transaction

# Create your views here.
# 1. Base View: Total control over the request
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {'title': 'Vault Home'})

# 2. TemplateView: Best for static pages
class AboutView(TemplateView):
    template_name = "about.html"

# 3. ListView: Automatically fetches all records of a model
class AccountListView(ListView):
    model = Account
    template_name = "account_list.html" # You would create this in templates/

# 4. CreateView: Handles form display and saving
class AccountCreateView(CreateView):
    model = Account
    fields = ['account_number', 'balance']
    success_url = '/accounts/'

#drf imports
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AccountSerializer, AccountDetailSerializer, TransactionSerializer

class AccountViewSet(viewsets.ModelViewSet):
    # Task 4: Override get_queryset to only show accounts owned by the logged-in user
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    # Task 4: Use different serializers for 'list' (basic) vs 'retrieve' (detail)
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AccountDetailSerializer
        return AccountSerializer

    # Task 3: Custom Action /api/accounts/{id}/freeze/
    @action(detail=True, methods=['post'])
    def freeze(self, request, pk=None):
        account = self.get_object()
        account.is_frozen = True
        account.save()
        return Response({'status': f'Account {account.account_number} has been frozen.'})

    # Task 3: Custom Action /api/accounts/{id}/statement/
    @action(detail=True, methods=['get'])
    def statement(self, request, pk=None):
        account = self.get_object()
        # Fetch transactions where this account is either sender or receiver
        sent = Transaction.objects.filter(sender=account)
        received = Transaction.objects.filter(receiver=account)
        all_tx = (sent | received).distinct()
        
        serializer = TransactionSerializer(all_tx, many=True)
        return Response(serializer.data)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # Task 3: Custom Action /api/transactions/{id}/reverse/
    @action(detail=True, methods=['post'])
    def reverse(self, request, pk=None):
        tx = self.get_object()
        if tx.is_reversed:
            return Response({'error': 'Already reversed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Logic: Swap the money back
        tx.sender.balance += tx.amount
        tx.receiver.balance -= tx.amount
        tx.is_reversed = True
        
        tx.sender.save()
        tx.receiver.save()
        tx.save()
        
        return Response({'status': 'Transaction has been successfully reversed.'})