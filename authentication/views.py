from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response


class RegisterAPIView(GenericAPIView):

    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "success": True,
            "message": "User succesfully registered.",
            "data": [serializer.data]
        }
        return Response(response, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):

    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "success": True,
            "message": "Login successfull.",
            "data": [serializer.data]
        }
        return Response(response, status=status.HTTP_200_OK)
