# Generated by Django 5.1.3 on 2024-11-17 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
        ('trail_logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='trail_log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trail_logs.traillog'),
        ),
    ]