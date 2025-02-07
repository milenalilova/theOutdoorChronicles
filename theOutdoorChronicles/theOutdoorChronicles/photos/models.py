from django.contrib.auth import get_user_model
from django.db import models

from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()


class Photo(models.Model):
    image = models.ImageField(
        upload_to='images/photo_uploads',
        null=False,
        blank=False
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    date_uploaded = models.DateTimeField(
        auto_now_add=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    trail = models.ForeignKey(
        Trail,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    animal = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='photos'
    )

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f"{self.trail.name}_{self.pk}"
