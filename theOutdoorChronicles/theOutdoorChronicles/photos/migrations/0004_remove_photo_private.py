# Generated by Django 5.1.3 on 2024-11-30 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_photo_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='private',
        ),
    ]
