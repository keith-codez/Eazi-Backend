# Generated by Django 5.1.6 on 2025-02-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_delete_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='middle_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
