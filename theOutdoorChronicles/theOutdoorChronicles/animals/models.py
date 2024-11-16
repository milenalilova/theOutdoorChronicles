from django.db import models

from theOutdoorChronicles.trails.models import Trail, TrailLog


class Animal(models.Model):
    image = models.ImageField(
        upload_to='images/animal_images',
        null=False,
        blank=False
    )

    common_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    species = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    conservation_status = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    description = models.TextField(
        null=False,
        blank=False
    )

    wikipedia_page = models.URLField(
        max_length=500,
        null=False,
        blank=False
    )

    additional_info = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )

    trails = models.ManyToManyField(Trail)

    trail_logs = models.ManyToManyField(
        TrailLog,
        blank=True
    )
