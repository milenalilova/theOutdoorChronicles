# Generated by Django 5.1.3 on 2024-11-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0001_initial'),
        ('trails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='trails',
            field=models.ManyToManyField(related_name='animals', to='trails.trail'),
        ),
    ]