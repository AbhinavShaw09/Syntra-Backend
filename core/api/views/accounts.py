from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.services import JwtService
from api.serializers import RegisterSerializer, LoginSerializer


class AuthViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if not user:
                return Response(
                    {"error": "User registration failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if not user:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            jwt_token = JwtService(user=user).get_token()

            return Response(
                {"access_token": str(jwt_token.access_token)},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
