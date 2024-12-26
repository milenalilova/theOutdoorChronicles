from django.contrib.auth import get_user_model
from django.db import models

from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.common.mixins import TimeStampMixin
from theOutdoorChronicles.photos.models import Photo
from theOutdoorChronicles.trail_logs.validators import validate_date_not_in_future
from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()


class TrailLog(TimeStampMixin, models.Model):
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    date_completed = models.DateField(
        validators=[validate_date_not_in_future],
        null=False,
        blank=False
    )

    duration = models.DurationField(
        null=True,
        blank=True
    )

    weather_conditions = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    trail_conditions = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    difficulty_rating = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    notes = models.TextField(
        null=False,
        blank=False
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='trail_logs'
    )

    trail = models.ForeignKey(
        Trail,
        on_delete=models.CASCADE,
        related_name='trail_logs'
    )

    animals = models.ManyToManyField(
        Animal,
        blank=True,
        related_name='trail_logs'
    )

    photos = models.ManyToManyField(
        Photo,
        blank=True,
        related_name='trail_logs'
    )

    class Meta:
        ordering = ['-date_completed']

    def __str__(self):
        return self.title
