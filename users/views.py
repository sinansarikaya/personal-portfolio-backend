from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        res = super().post(request, *args, **kwargs)
        res.set_cookie("access_token", serializer.validated_data["access"], httponly=True)
        res.set_cookie("refresh_token", serializer.validated_data["refresh"], httponly=True)

        return res

class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Retrieve refresh token from cookies
        cookie = request.COOKIES.get('refresh_token')

        if not cookie:
            return Response({'error': 'Refresh token not found'}, status=status.HTTP_401_UNAUTHORIZED)

        request.data.update({'refresh': cookie})

        return super().post(request, *args, **kwargs)

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        data = serializer.data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        # add other fields as needed
    }
    return Response(data, status=status.HTTP_200_OK)
   

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response()
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
