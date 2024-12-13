from rest_framework import serializers
from .models import Doctor, Schedule, Appointment

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'   