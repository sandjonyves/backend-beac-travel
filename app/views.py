from django.shortcuts import get_object_or_404


from rest_framework import viewsets
from .models import Service, Agency, Mission, Trip
from .serializers import ServiceSerializer, AgencySerializer, MissionSerializer, TripSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

   

    @action(detail=False, methods=['get'], url_path='user-agency/(?P<admin_id>[^/.]+)')
    def admin_agency(self, request, admin_id):
        # Retrieve the agency associated with the given admin_id
        try:
            agency = self.queryset.get(admin_user__id=admin_id)
            serializer = self.get_serializer(agency)
            return Response(serializer.data)
        except Agency.DoesNotExist:
            return Response({"detail": "Agency not found."}, status=404)
        
    @action(detail=False, methods=['get'], url_path='service-agencies/(?P<service_id>[^/.]+)')
    def agency_service(self, request, service_id):
        # Retrieve the agency associated with the given admin_id
        try:
            agency = self.queryset.filter(service__id=service_id)
            serializer = self.get_serializer(agency,many=True)
            return Response(serializer.data)
        except Agency.DoesNotExist:
            return Response({"detail": "Agency not found."}, status=404)


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @action(detail=False, methods=['get'], url_path='user-missions/(?P<user_id>\w+)')
    def user_missions(self, request, user_id):
        missions = self.queryset.filter(user__id=user_id)
        serializer = self.get_serializer(missions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user-request/(?P<service_id>\w+)')
    def user_requests(self, request, service_id):
        missions = self.queryset.filter(
            status='submitted',
            user__agency__service__id=service_id
        )
        serializer = self.get_serializer(missions, many=True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['put'], url_path='status-change/(?P<mission_status>\w+)')
    def status_change(self, request, pk=None, mission_status=None):
        mission = self.get_object()  
        mission.status = mission_status  
        mission.save()  


    @action(detail=True, methods=['delete'], url_path='delete-trips')
    def delete_trips_mission(self, request, pk=None):
        mission = self.get_object() 
        mission.trips.all().delete()  # Supprime tous les trajets associés à la mission

        return Response({'detail': 'Tous les trajets de la mission ont été supprimés.'}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(mission)  
        return Response(serializer.data, status=status.HTTP_200_OK) 

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    @action(detail=False, methods=['get'], url_path=r'mission-trips/(?P<mission_id>\d+)')
    def mission_trips(self, request, mission_id):
        # Retrieve the mission using get_object_or_404 for better error handling
        mission = get_object_or_404(Mission, id=mission_id)

        # Retrieve trips associated with this mission
        trips = self.queryset.filter(mission_id=mission_id)

        # Check if all trips are completed
        if trips.exists() and all(trip.status == 'completed' for trip in trips):
            mission.status = 'finish'
            mission.save()

        # Serialize and return the data
        serializer = self.get_serializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def validate_trip(self, request, pk=None):
        trip = self.get_object()
        trip.status = 'completed'
        trip.save()
        serializer = self.get_serializer(trip)
        return Response(serializer.data)
    
    # @action(detail=False,methods='delete' , url_name='delete-trips-mission/?Pmission_id'):
    # def delete_trips_mission