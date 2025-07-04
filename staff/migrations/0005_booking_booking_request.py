# Generated by Django 5.1.6 on 2025-07-02 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0001_initial'),
        ('staff', '0004_booking_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_request',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='rentals.bookingrequest'),
            preserve_default=False,
        ),
    ]
