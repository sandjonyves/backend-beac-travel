from django.db import models
from datetime import date
from django.utils import timezone  # Pour gérer correctement les dates

# Remplacer l'importation de CustomUser par une chaîne de caractères
class Service(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=50)
    description = models.TextField(null=True)
    # mission = models.TextField()

    def __str__(self):
        return self.name

class Agency(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='agencies')
    country = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone

class Mission(models.Model):
    STATUS_CHOICES = [
        ('in creation', 'In Creation'),
        ('submitted', 'Submitted'),     
        ('approved', 'Approved'),
        ('in progress', 'In Progress'),
        ('rejected', 'Rejected'),
        ('failure', 'Failure'),
        ('finish', 'Finish'),
    ]

    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='missions')
    orderNumber = models.CharField(max_length=255)
    description = models.TextField(null=True)
    duration = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Ajout de blank=True pour éviter les erreurs dans les formulaires
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in creation')

    def __str__(self):
        return f"Mission {self.id} - {self.description or 'No Description'}"

    @classmethod
    def update_status(cls, missions=[]):
        for mission in missions:
            if mission.status!='finish' or mission.status != 'failed':

                if mission.status == 'approved' and timezone.now().date() > mission.start_date:
                    mission.status = 'in progress'
                
                    mission.save()
                # elif 
    # @classmethod
    # def 
 

class Trip(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('completed', 'completed'),
    ]
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True, related_name='trips')
    grade = models.CharField(max_length=128)
    departure_city = models.CharField(max_length=255, blank=True, null=True)
    arrival_city = models.CharField(max_length=255, blank=True, null=True)
    accommodation = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Trip {self.id} - {self.departure_city} to {self.arrival_city}"