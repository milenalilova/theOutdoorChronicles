from django.db import models


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
