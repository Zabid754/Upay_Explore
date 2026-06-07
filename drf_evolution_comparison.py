"""
DELIVERABLE: DRF View Comparison
This file demonstrates three ways to implement the same 'Account List' endpoint.
"""
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from vault.models import Account
from vault.serializers import AccountSerializer

# STYLE 1: APIView
class AccountListAPIView(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    """
    TRADEOFF: 
    - Pros: Total control over the logic. 
    - Cons: You have to write everything manually (serialization, response, status codes).
    """

# STYLE 2: GenericAPIView (with ListCreateAPIView)
class AccountGenericAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    """
    TRADEOFF: 
    - Pros: Extremely fast to write for standard CRUD. 
    - Cons: Slightly harder to customize the core behavior compared to APIView.
    """

# STYLE 3: ModelViewSet
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    """
    TRADEOFF: 
    - Pros: Handles ALL CRUD operations (List, Create, Retrieve, Update, Delete) in one class. 
    - Cons: Sometimes feels like "too much magic" if you only need one or two methods.
    """