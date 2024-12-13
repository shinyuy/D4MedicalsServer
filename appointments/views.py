from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Doctor, Schedule, Appointment
from .serializers import DoctorSerializer, ScheduleSerializer, AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]  # Open to all for booking