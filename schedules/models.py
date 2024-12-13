from django.db import models

# Create your models here.
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default='available')  # or 'booked'