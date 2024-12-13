from django.db import models

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    specialties = models.JSONField()  # e.g., ['Taxi', 'HGV']