from django.db import models

# Create your models here.
class Appointment(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=15)
    appointment_type = models.CharField(max_length=50)  # Taxi, HGV, etc.
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=15, default='pending')  # pending, completed