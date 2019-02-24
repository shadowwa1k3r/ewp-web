from rest_framework import generics, permissions, status
from .models import Council, EwpUser, Feedback, Aviarace, Apartment
from rest_framework.response import Response
from .serializers import CouncilSerializer, TokenSerializer, AviaraceListSerializer, ApartmentListSerializer
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


class FeedbackCreateView(generics.CreateAPIView):
    allowed_methods = ['post']
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        name = request.data.get('username')
        email = request.data.get('email')
        title = request.data.get('title')
        message = request.data.get('message')
        Feedback.objects.create(user=user, name=name, email=email, title=title, message=message)
        return Response(status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    allowed_methods = ['post']
    permission_classes = (permissions.AllowAny,)
    query_set = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        confirm_code = request.data.get('confirm_code', '')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        print(user)
        if not confirm_code:
            if user is not None:
                gen_code = EwpUser.generate_confirm_code()
                user.ewpuser.confirm_code = gen_code
                user.ewpuser.save()
                print('gen for existing user')
                EwpUser.send_confirm_code(username, gen_code)
                return Response(status=status.HTTP_200_OK)
            else:
                gen_code = EwpUser.generate_confirm_code()
                cuser = User(username=username)
                cuser.save()
                cuser.ewpuser.confirm_code = gen_code
                cuser.ewpuser.save()
                print('gen for new user')
                EwpUser.send_confirm_code(username, gen_code)
                return Response(status=status.HTTP_200_OK)
        else:
            if user:
                print('gen token')
                if confirm_code == user.ewpuser.confirm_code:
                    serializer = TokenSerializer(data={
                        'token': jwt_encode_handler(
                            jwt_payload_handler(user)
                        )
                    })
                    serializer.is_valid()
                    return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListAviaraceView(generics.ListAPIView):

    def get_serializer_class(self):
        return AviaraceListSerializer

    def get_queryset(self):
        city = self.request.GET.get("city")
        qs = Aviarace.objects.all()
        if city:
            qs = qs.filter(city__icontains=city)
        return qs


class ListApartmentAPIView(generics.ListAPIView):
    def get_queryset(self):
        ned_type = self.request.GET.get("ned_type")  # nedvigimost_type

        qs = Apartment.objects.all()

        if ned_type:
            qs = qs.filter(nedvigimost_type__icontains=ned_type)
        return qs

    def get_serializer_class(self):
        return ApartmentListSerializer
