from ..models import User
from django.contrib.auth import login
from django.db import transaction
# Rest FrameWork
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView
from knox.models import AuthToken
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class Home(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "Hello User ": str(request.user)
        })


class SignUp(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class SignIn(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            return Response({
                "message": "User do not verify email"
            })
        login(request, user)
        return super(SignIn, self).post(request, format=None)


class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Use Information in Swagger",
        responses={
            status.HTTP_200_OK: UserSerializer()
        }
    )
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

