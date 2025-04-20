from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError

class Vehicle(models.Model):
    id = models.IntegerField(primary_key=True)  # Assuming ID is unique and primary key
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('In-Transit', 'In-Transit'),
                                                       ('Delivered', 'Delivered')])
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)  # GPS Coordinates
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

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
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    last_scanned_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

    def clean(self):
        """Override the clean method to validate vehicle."""
        if self.vehicle and not Vehicle.objects.filter(id=self.vehicle.id).exists():
            raise ValidationError(f"Vehicle with id {self.vehicle.id} does not exist.")
    
    def save(self, *args, **kwargs):
        """Override the save method to ensure vehicle integrity."""
        # Run the validation for the vehicle before saving
        self.clean()
        super(Product, self).save(*args, **kwargs)
