from django.db import models

class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    plate_number = models.CharField(max_length=20, unique=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name
