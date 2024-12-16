from django.db import models

class Center(models.Model):
    center_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    earliest_date = models.DateField()
    # parking = models.BooleanField(default=False)
    full_address = models.TextField()
    open_from = models.TimeField()
    closes_at = models.TimeField()
    center_calendar_id = models.CharField(max_length=255)

    def __str__(self):
        return self.center_name
