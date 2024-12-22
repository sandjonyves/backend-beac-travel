from rest_framework import serializers
from .models import Service, Agency, Mission, Trip

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class MissionSerializer(serializers.ModelSerializer):
    trips = TripSerializer(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = '__all__'

class AgencySerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    missions = MissionSerializer(many=True, read_only=True)

    class Meta:
        model = Agency
        fields = '__all__'