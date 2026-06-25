from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import UserSession
from authentication.serializers import UserSessionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

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

#using ApiView

class ActiveSessionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = UserSession.objects.filter(
            user=request.user, 
            is_active=True
        ).order_by('-created_at')
        serializer = UserSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RevokeSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        session = get_object_or_404(UserSession, pk=pk, user=request.user)
        try:
            token = RefreshToken(session.refresh_token)
            token.blacklist()
        except Exception:
            pass
        session.is_active = False
        session.save()
        return Response(
            {"message": "Device access revoked"}, 
            status=status.HTTP_204_NO_CONTENT
        )