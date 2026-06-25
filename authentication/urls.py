from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import RegisterView, LoginView, LogoutView, ActiveSessionsView, RevokeSessionView, RegisterAPIView, LoginAPIView, LogoutAPIView, ActiveSessionsAPIView, RevokeSessionAPIView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('sessions/', ActiveSessionsView.as_view(), name='sessions'),
    path('sessions/<int:pk>/revoke/', RevokeSessionView.as_view(), name='revoke_session'),

    path('register-api/', RegisterAPIView.as_view(), name='register-api'),
    path('login-api/', LoginAPIView.as_view(), name='login-api'),
    path('logout-api/', LogoutAPIView.as_view(), name='logout-api'),

    path('sessions-api/', ActiveSessionsAPIView.as_view(), name='sessions-api'),
    path('sessions-api/<int:pk>/revoke/', RevokeSessionAPIView.as_view(), name='revoke-api'),
]