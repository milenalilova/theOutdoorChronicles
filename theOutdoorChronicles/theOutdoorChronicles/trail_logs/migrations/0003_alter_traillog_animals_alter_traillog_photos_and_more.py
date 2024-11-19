# Generated by Django 5.1.3 on 2024-11-19 15:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0002_alter_animal_trails'),
        ('photos', '0002_alter_photo_animal_alter_photo_trail_and_more'),
        ('trail_logs', '0002_traillog_animals_traillog_photos'),
        ('trails', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='traillog',
            name='animals',
            field=models.ManyToManyField(blank=True, related_name='trail_logs', to='animals.animal'),
        ),
        migrations.AlterField(
            model_name='traillog',
            name='photos',
            field=models.ManyToManyField(blank=True, related_name='trail_logs', to='photos.photo'),
        ),
        migrations.AlterField(
            model_name='traillog',
            name='trail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trail_logs', to='trails.trail'),
        ),
        migrations.AlterField(
            model_name='traillog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trail_logs', to=settings.AUTH_USER_MODEL),
        ),
    ]
