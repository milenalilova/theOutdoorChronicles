# Generated by Django 5.1.3 on 2024-11-15 09:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('animals', '0001_initial'),
        ('trails', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/photo_uploads')),
                ('description', models.TextField(blank=True, null=True)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('animal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='animals.animal')),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trails.trail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
