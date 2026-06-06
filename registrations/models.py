from django.db import models

# Create your models here.
class Registration(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CANCELLED', 'Cancelled')
    ]

    username = models.CharField(max_length=100)

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    registered_at = models.DateTimeField(auto_now_add=True)
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['username', 'event'],
            name='unique_user_event'
        )
    ]