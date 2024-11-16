# Generated by Django 5.1.3 on 2024-11-16 10:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trails', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('date_completed', models.DateField()),
                ('duration', models.DurationField(blank=True, null=True)),
                ('weather_conditions', models.CharField(blank=True, max_length=100, null=True)),
                ('trail_conditions', models.CharField(blank=True, max_length=100, null=True)),
                ('difficulty_rating', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.TextField()),
                ('private', models.BooleanField(default=False)),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trails.trail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_completed'],
            },
        ),
    ]
