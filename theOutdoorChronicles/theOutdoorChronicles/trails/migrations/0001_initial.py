# Generated by Django 5.1.3 on 2024-11-15 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/trails_images/')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('length', models.DecimalField(decimal_places=2, max_digits=5)),
                ('elevation_gain', models.PositiveIntegerField()),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Hard', 'Hard')], max_length=50)),
                ('route_type', models.CharField(choices=[('Loop', 'Loop'), ('One Way', 'One Way')], max_length=50)),
                ('description', models.TextField()),
            ],
        ),
    ]
