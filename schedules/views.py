from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Doctor, Schedule, Appointment
from .serializers import DoctorSerializer, ScheduleSerializer, AppointmentSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]