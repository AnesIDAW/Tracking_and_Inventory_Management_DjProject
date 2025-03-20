from django.db import models
from users.models import CustomUser

class Product(models.Model):
    STATUS_CHOICES = [
        ('stored', 'Stored'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ]

    name = models.CharField(max_length=255)
    rfid_tag = models.CharField(max_length=100, unique=True)  # RFID identifier
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='stored')
    warehouse_location = models.CharField(max_length=255, null=True, blank=True)
    vehicle = models.ForeignKey('tracking.Vehicle', null=True, blank=True, on_delete=models.SET_NULL)
    last_scanned_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
