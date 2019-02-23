from rest_framework import generics, permissions, status
from .models import Council
from rest_framework.response import Response
from .serializers import CouncilSerializer, TokenSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListCouncilView(generics.ListAPIView):
    """
    Provides a get method handler
    """
    allowed_methods = ['get']
    queryset = Council.objects.all()
    serializer_class = CouncilSerializer
    permission_classes = (permissions.IsAuthenticated,)


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    allowed_methods = ['post']
    permission_classes = (permissions.AllowAny,)

    query_set = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        # password = request.data.get('password', '')
        user = authenticate(username=username)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                'token': jwt_encode_handler(
                    jwt_payload_handler(user)
                )
            })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """

    allowed_methods = ['post']
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        email = request.data.get('email', '')
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(status=status.HTPP_201_CREATED)
