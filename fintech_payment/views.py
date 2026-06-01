from django.shortcuts import render
from .models import Transaction

# Create your views here.
def optimization_view(request):
    # UNCOMMENT one at a time to see the difference in Debug Toolbar
    
    # Version 1: SLOW (N+1 Queries)
    transactions = Transaction.objects.all() 
    
    # Version 2: FAST (1 Query)
    #transactions = Transaction.objects.select_related('sender__user', 'merchant').all()

    return render(request, 'optimization.html', {'transactions': transactions})