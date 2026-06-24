# authentication/views/auth_views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import RegisterSerializer, MyTokenObtainPairSerializer
from authentication.models import UserSession
from rest_framework_simplejwt.exceptions import TokenError

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user 
        token_data = serializer.validated_data
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
        ip_address = request.META.get('REMOTE_ADDR')
        UserSession.objects.create(
            user=user, 
            ip_address=ip_address,
            user_agent=user_agent,
            refresh_token=token_data['refresh']
        )

        return Response(token_data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            UserSession.objects.filter(refresh_token=refresh_token).update(is_active=False)
            return Response({"message": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid token"},status=status.HTTP_400_BAD_REQUEST)