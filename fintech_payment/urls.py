from django.urls import path
from . import views

urlpatterns = [
    # This matches: http://127.0.0.1:8000/fintech/test-optimization/
    path('test-optimization/', views.optimization_view, name='optimization_test'),
]