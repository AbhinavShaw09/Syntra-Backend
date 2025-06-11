# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class HelloWorldView(APIView):
    authentication_classes = []  # disables authentication (including JWT)
    permission_classes = [AllowAny]  # allows all requests
    def get(self, request):
        return Response({"message": "Hello, World!"})
