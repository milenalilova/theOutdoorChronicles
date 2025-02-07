from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

UserModel = get_user_model()


class Trail(models.Model):
    class TrailDifficultyChoices(models.TextChoices):
        DIFFICULTY_EASY = 'Easy', 'Easy'
        DIFFICULTY_MODERATE = 'Moderate', 'Moderate'
        DIFFICULTY_HARD = 'Hard', 'Hard'

    class RouteTypeChoices(models.TextChoices):
        TYPE_LOOP = 'Loop', 'Loop'
        TYPE_ONE_WAY = 'One Way', 'One Way'

    image = models.ImageField(
        upload_to='images/trails_images/',
        null=False,
        blank=False
    )

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    location = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    length = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=False,
        blank=False
    )

    elevation_gain = models.PositiveIntegerField(
        null=False,
        blank=False
    )

    difficulty = models.CharField(
        max_length=50,
        choices=TrailDifficultyChoices.choices,
        null=False,
        blank=False
    )

    route_type = models.CharField(
        max_length=50,
        choices=RouteTypeChoices.choices,
        null=False,
        blank=False
    )

    description = models.TextField(
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('trail-details', kwargs={'trail_id': self.pk})

    def __str__(self):
        return f"{self.name}, {self.location}"
