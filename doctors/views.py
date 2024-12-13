from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Doctor, Schedule, Appointment
from .serializers import DoctorSerializer, ScheduleSerializer, AppointmentSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]