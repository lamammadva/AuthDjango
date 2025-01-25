from django.shortcuts import render
from rest_framework import status,exceptions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from drf_yasg import openapi
def check_if_token_blacklisted(token):
    try:
        BlacklistedToken.objects.get(token=token)
        return True
    except BlacklistedToken.DoesNotExist:
        return False
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(
            serializer.data    

        )

class RegisterView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            status.HTTP_201_CREATED: RegisterSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response(
                {
                    'message': 'User registered successfully',
                    'access_token': str(token.access_token),
                    'refresh_token': str(token),
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer






class GoogleLoginAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Google OAuth login",
        responses={200: openapi.Response('Successful response', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
            }
        ))}
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })