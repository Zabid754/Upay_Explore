"""
DELIVERABLE: Django View Comparison
This file demonstrates the implementation of traditional Django Class-Based Views (CBVs)
and explains the use cases for each.
"""

from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from vault.models import Account

# 1. Base View
class MyBaseView(View):
    def get(self, request):
        pass
    """
    WHEN TO CHOOSE:
    Use the base 'View' when you need total control over the request logic. 
    It doesn't provide any "magic" shortcuts, making it perfect for custom logic 
    that doesn't fit into standard CRUD (like a complex dashboard).
    """

# 2. TemplateView
class HomeTemplateView(TemplateView):
    template_name = "home.html"
    """
    WHEN TO CHOOSE:
    Use 'TemplateView' for static pages or pages with very simple data requirements. 
    It is the fastest way to render a template that doesn't rely heavily on database objects.
    """

# 3. ListView
class AccountListView(ListView):
    model = Account
    """
    WHEN TO CHOOSE:
    Use 'ListView' whenever you need to display a collection of objects. 
    It automatically handles fetching all records from the database and 
    provides pagination features out of the box.
    """

# 4. CreateView
class AccountCreateView(CreateView):
    model = Account
    fields = ['account_number', 'balance']
    """
    WHEN TO CHOOSE:
    Use 'CreateView' for 'Add Item' pages. It automatically generates a form 
    based on your model, handles the POST data validation, and saves the 
    new object to the database if the data is valid.
    """

# 5. UpdateView & DeleteView
class AccountUpdateView(UpdateView):
    model = Account
    fields = ['is_frozen']

class AccountDeleteView(DeleteView):
    model = Account
    success_url = '/accounts/'
    """
    WHEN TO CHOOSE:
    Use these for administrative actions. UpdateView is perfect for editing 
    existing profiles or settings, and DeleteView provides the logic for 
    removing records with a confirmation step.
    """