# Generated by Django 5.1.3 on 2024-11-30 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trail_logs', '0003_alter_traillog_animals_alter_traillog_photos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traillog',
            name='private',
        ),
    ]
