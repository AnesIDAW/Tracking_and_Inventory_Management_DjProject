from django.db import models

class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    plate_number = models.CharField(max_length=20, unique=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)  # GPS Coordinates
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
