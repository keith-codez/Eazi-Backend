# Generated by Django 5.1.6 on 2025-04-18 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0016_alter_manager_groups_alter_manager_middle_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='username',
        ),
    ]
