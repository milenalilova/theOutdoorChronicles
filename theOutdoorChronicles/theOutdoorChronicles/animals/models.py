from django.db import models
from django.urls import reverse

from theOutdoorChronicles.trails.models import Trail


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

    trails = models.ManyToManyField(
        Trail,
        related_name='animals'
    )

    def get_absolute_url(self):
        return reverse('animal-details', kwargs={'animal_id': self.pk})

    def __str__(self):
        return f"{self.species}; {self.common_name}"
