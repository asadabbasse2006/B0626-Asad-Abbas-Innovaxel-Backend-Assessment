from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    total_seats = models.PositiveIntegerField()

    available_seats = models.PositiveIntegerField()

    event_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )