# Generated by Django 5.1.7 on 2025-03-24 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
