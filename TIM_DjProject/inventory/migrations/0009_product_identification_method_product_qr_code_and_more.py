# Generated by Django 5.1.7 on 2025-06-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_rename_lat_vehicle_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='identification_method',
            field=models.CharField(choices=[('RFID', 'RFID'), ('QR', 'QR Code')], default='RFID', max_length=4),
        ),
        migrations.AddField(
            model_name='product',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
        migrations.AddField(
            model_name='product',
            name='ticket',
            field=models.FileField(blank=True, null=True, upload_to='tickets/'),
        ),
    ]
