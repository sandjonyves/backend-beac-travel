from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, AgencyViewSet, MissionViewSet, TripViewSet


router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'agencies', AgencyViewSet)
router.register(r'missions', MissionViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('', include(router.urls)),
]