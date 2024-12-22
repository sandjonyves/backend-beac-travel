from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Admin, Agent, Superuser, CustomUser
from app.serializers import AgencySerializer
from app.models import Agency
# Sérialiseur pour CustomUser
class UserSerializer(serializers.ModelSerializer):
    # agency = AgencySerializer(read_o)
    # agency_detail = AgencySerializer(source='agency', read_only=True)  # Détail de l'agence

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'password', 'role')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

# Sérialiseur pour Agent
class AgentSerializer(serializers.ModelSerializer):

    agency_detail = AgencySerializer(source='agency', read_only=True) 

    class Meta:
        model = Agent
        fields = ('id', 'username', 'admin_id', 'email', 'phone_number', 'password', 'role', 'agency','agency_detail')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        agent = super().create(validated_data)
        if password:
            agent.set_password(password)
        agent.save()
        return agent

# Sérialiseur pour Admin
class AdminSerializer(serializers.ModelSerializer):
    agency = serializers.PrimaryKeyRelatedField(queryset=Agency.objects.all(), required=False)

    class Meta:
        model = Admin
        fields = '__all__'

# Sérialiseur pour Superuser
class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Superuser
        fields = '__all__'

# Sérialiseur pour la connexion utilisateur
class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        # Ajoutez ici une validation supplémentaire si nécessaire
        return super().validate(attrs)