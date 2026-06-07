"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  
from rest_framework.routers import DefaultRouter
from vault.views import (
    HomeView, AboutView, AccountListView, AccountCreateView,
    AccountViewSet, TransactionViewSet 
)

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('accounts-web/', AccountListView.as_view(), name='account-list-web'),
    path('accounts-web/add/', AccountCreateView.as_view(), name='account-add-web'),

    path('api/', include(router.urls)),
]
