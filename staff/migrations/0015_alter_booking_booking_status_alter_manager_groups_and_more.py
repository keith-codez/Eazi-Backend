# Generated by Django 5.1.6 on 2025-04-10 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('staff', '0014_alter_booking_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_status',
            field=models.CharField(choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('completed', 'Completed'), ('active', 'Active'), ('canceled', 'Canceled')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='manager',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='manager_users', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='manager_user_permissions', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
