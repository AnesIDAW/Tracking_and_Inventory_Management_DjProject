# Generated by Django 5.1.7 on 2025-04-27 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_remove_vehicle_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='lat',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='long',
            new_name='longitude',
        ),
    ]
