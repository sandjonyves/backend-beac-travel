from django.db import transaction
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from .serializer import *
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, viewsets, mixins
from rest_framework_simplejwt.tokens import RefreshToken

class PersonalModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass

def create_admin(validated_data):
    return Admin.objects.create(
        is_superuser=True,
        is_staff=True,
        **validated_data
    )

def create_Agent(validated_data):
    return Agent.objects.create(
        is_staff=True,
        **validated_data
    )

def create_client(validated_data):
    return Client.objects.create(
        **validated_data
    )

class UserRegister(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            role = serializer.validated_data.get('role')
            password = serializer.validated_data.pop('password')

            # Hash the password
            serializer.validated_data['password'] = make_password(password)

            # Create the user based on role
            if role == Admin.Role.ADMIN:
                user = create_admin(serializer.validated_data)
            elif role == Agent.Role.Agent:
                user = create_Agent(serializer.validated_data)
            else:
                user = create_client(serializer.validated_data)

            if user is None:
                return Response({'message': _('Error: User could not be created.')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user = authenticate(email=user.email, password=password)

            if not user or not user.is_active:
                raise serializers.ValidationError(_('Invalid credentials or user inactive.'))

            login(request, user)
            token = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(token),
                'access': str(token.access_token),
                'message': _('User created successfully.'),
                'role': user.role,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'id': user.id,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({'message': _('Invalid data.')}, status=status.HTTP_400_BAD_REQUEST)

class AgentUser(PersonalModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()

class AdminUser(PersonalModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()

class ClientUser(PersonalModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

class OtherClientView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = OtherClientSerializer
    queryset = OtherClient.objects.all()

class UserLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
            return Response({'message': _('Invalid credentials or user inactive.')}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        token = RefreshToken.for_user(user)

        response_data = {
            'refresh': str(token),
            'access': str(token.access_token),
            'message': _('User logged in successfully.'),
            'role': user.role,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'id': user.id,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class Logout(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({'message': _('Logout successful.')}, status=status.HTTP_200_OK)

class SendMail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        subject = _("Contact from e-commerce application")
        message = request.data.get('message')
        receive_mail = request.data.get('email')
        name = request.data.get('fullName')

        if not receive_mail:
            return Response({'message': _('Please verify your information.')}, status=status.HTTP_400_BAD_REQUEST)

        full_message = f"{name}\n\n{message}"
        send_mail(subject, full_message, 'sandjonyves@gmail.com', [receive_mail])

        return Response({'message': _('Message sent successfully.')}, status=status.HTTP_200_OK)




        class Logout(APIView):
permission_classes=[AllowAny]

class Logout(APIView):
permission_classes=[AllowAny]
def post(self, request,id):
user = CustomUser.objects.filter(id=id).first
request.user = user
# print(request.user)
logout(request)
if not request.user.is_authenticated: