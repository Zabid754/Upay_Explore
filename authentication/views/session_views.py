# authentication/views/session_views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import UserSession
from authentication.serializers import UserSessionSerializer
from rest_framework.permissions import IsAuthenticated

class ActiveSessionsView(generics.ListAPIView):
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user, 
            is_active=True
        ).order_by('-created_at')

class RevokeSessionView(generics.DestroyAPIView):
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            token = RefreshToken(instance.refresh_token)
            token.blacklist()
        except Exception:
            pass
        instance.is_active = False
        instance.save()