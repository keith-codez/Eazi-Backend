# Generated by Django 5.1.6 on 2025-06-05 15:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('regulator', '0001_initial'),
        ('staff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('pickup_time', models.TimeField(blank=True, null=True)),
                ('dropoff_time', models.TimeField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=20)),
                ('staff_notes', models.TextField(blank=True, null=True)),
                ('is_confirmed_by_customer', models.BooleanField(default=False)),
                ('customer_docs_submitted', models.BooleanField(default=False)),
                ('dummy_payment_done', models.BooleanField(default=False)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(blank=True, help_text='Agent who accepted this request', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_requests', to='regulator.agent')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_requests', to='regulator.customer')),
                ('dropoff_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dropoff_requests', to='staff.location')),
                ('pickup_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pickup_requests', to='staff.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_requests', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_requests', to='staff.vehicle')),
            ],
        ),
    ]
