from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password
from .serializer import *
from .models import *

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, viewsets, mixins
from .models import RevokedToken
from rest_framework.decorators import action
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






class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        user, token = super().authenticate(request)
        if token and RevokedToken.objects.filter(token=token).exists():
            raise AuthenticationFailed("Token has been revoked.")
        
        # Uncomment if you want to check for token expiration
        # if token and token.is_expired():
        #     raise AuthenticationFailed("Token has expired.")
        
        return (user, token)


def create_admin(validated_data):
    return Admin.objects.create(
        is_staff=True,
        **validated_data
    )

def create_agent(validated_data):
    return Agent.objects.create(
        is_staff=True,
        **validated_data
    )

def create_superuser(validated_data):
    return Superuser.objects.create(
        is_superuser=True,
        is_staff=True,
        **validated_data
    )

class UserRegister(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            role = serializer.validated_data.get('role')
            password = serializer.validated_data.pop('password')

            # Hash the password
            serializer.validated_data['password'] = make_password(password)

            # Create the user based on role
            if role == CustomUser.Role.SUPERUSER:
                user = create_superuser(serializer.validated_data)
            elif role == CustomUser.Role.ADMIN:
                user = create_admin(serializer.validated_data)
            else:
                user = create_agent(serializer.validated_data)

            if user is None:
                return Response({'message': _('Error: User could not be created.')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

           
            login(request, user)

            

            # if hasattr(user, 'admin') or hasattr(user, 'agent'):
            #     user_info['agency'] = user.agency  
            # elif hasattr(user, 'superuser'):
            #     user_info['service'] = user.service  

           
            token = RefreshToken.for_user(user)
            user.refresh_token = str(token) 
            user.save() 
            user_info = {
                'id':user.id,
                # 'username': user.username,
                # 'email': user.email,
                # 'phone_number': user.phone_number,
                'role': user.role,
            }

            response_data = {
                'access': str(token.access_token),
                'refresh': str(token),  
                'user': user_info,
                'message': _('User created successfully.'),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({'message': _('Invalid data.')}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'], 
            url_path=r'update-grade/(?P<user_id>\d+)/(?P<grade>\w+)')
    def update_grade(self, request, user_id, grade):
        try:
            user = CustomUser.objects.get(id=int(user_id))
            user.grade = grade
            user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'message': _('User not found.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AgentUser(PersonalModelViewSet):
    permission_classes = [AllowAny]
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    

    # @action(detail=False, methods=['get'], url_path='users-agency/(?P<user_id>\w+)')
    # def user_agency(self, request,user_id):
    #     mission = self.queryset.get(user__id=user_id)
    #     return JsonResponse(mission, safe=False)


    @action(detail=False, methods=['get'], url_path=r'users-agency/(?P<agency_id>\d+)')
    def users_agency(self, request, agency_id):
        # Retrieve all agents belonging to the specified agency
        agents = self.queryset.filter(agency__id=agency_id)

        # Return 404 if no agents are found
        if not agents.exists():
            return Response(
                {"detail": "No users found for the specified agency."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize and return the data
        serializer = self.get_serializer(agents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)







class AdminUser(PersonalModelViewSet):
    permission_classes = [AllowAny]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    



 
  

class SuperUser(PersonalModelViewSet):
    permission_classes = [AllowAny]
    queryset = Superuser.objects.all()
    serializer_class = SuperUserSerializer
    



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
        # token['role'] = user.role 
     
        # if hasattr(user, 'admin') or hasattr(user, 'agent'):
        #     user_info['agency'] = user.agency  
        # elif hasattr(user, 'superuser'):
        #     user_info['service'] = user.service 
        user_info = {
            'id':user.id,
            # 'username': user.username,
            # 'email': user.email,
            # 'phone_number': user.phone_number,
            # 'agency':user.agency,
            'role': user.role,
        }

      
        response_data = {
            'access': str(token.access_token), 
            'user': user_info, 
            'message': _('User logged in successfully.')
        }

        return Response(response_data, status=status.HTTP_200_OK)

# class Logout(APIView):
#     permission_classes=[AllowAny]
#     def post(self, request,id):
#         user =  CustomUser.objects.filter(id=id).first()
#         # print(id)
#         if user:
#             request.user = user
#             print(request.user)
#             logout(request)
#             if not request.user.is_authenticated:

#                 return Response({
#                 'message': 'logout succesfull'
#                 }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#             'message': 'logout failed'
#             })


class Logout(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # token = request.headers.get('Authorization').split(' ')[1]

            # revoked_token = RevokedToken(token=token)
            # revoked_token.save()

            logout(request)

            return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)



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