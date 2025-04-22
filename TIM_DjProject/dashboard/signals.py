from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import Product
from .utils import send_delivery_notification

@receiver(post_save, sender=Product)
def delivered_notify(sender, instance, **kwargs):
    if instance.status == 'delivered':
        send_delivery_notification(instance)