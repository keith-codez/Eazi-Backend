# Generated by Django 5.1.6 on 2025-03-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_vehicle_registration_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='price_per_day',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
