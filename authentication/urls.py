from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import RegisterView, LoginView, LogoutView, ActiveSessionsView, RevokeSessionView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('sessions/', ActiveSessionsView.as_view(), name='sessions'),
    path('sessions/<int:pk>/revoke/', RevokeSessionView.as_view(), name='revoke_session'),
]