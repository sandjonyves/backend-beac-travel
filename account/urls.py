from django.urls import path,include
from .views import *
from rest_framework import routers

route =routers.SimpleRouter()

route.register('register',UserRegister,basename='user')



route.register('agent',AgentUser,basename='Agent')
route.register('admin',AdminUser,basename='admin')
route.register('superuser',SuperUser,basename='superuser')

urlpatterns =[
    
    path('',include(route.urls)),
   

    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
]