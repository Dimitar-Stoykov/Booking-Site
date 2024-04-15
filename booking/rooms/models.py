from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from booking.hotels.models import Hotel


UserModel = get_user_model()


class Room(models.Model):

    room_number = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    price_per_night = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=False,
        blank=False,
    )

    capacity = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms',
    )

    def __str__(self):
        return f"Room {self.room_number}"


class RoomPictures(models.Model):

    image = models.URLField(
        null=False,
        blank=False,
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='pictures',
    )


