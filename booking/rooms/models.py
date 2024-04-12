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
    # TODO: check it is unnessesary when creating booking
    # booked_by = models.ForeignKey(
    #     UserModel,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='booked_rooms',
    # )
    def __str__(self):
        return f"Room {self.room_number}"

class RoomPictures(models.Model):

    image = models.URLField()

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='pictures',
    )


class Booking(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):

        if Booking.objects.filter(room=self.room, start_date__lte=self.end_date, end_date__gte=self.start_date).exists():
            # If the room is already booked for any overlapping period, raise ValidationError
            raise ValidationError('This room is already booked for the specified period.')
        # If the room is available, save the Booking instance
        super().save(*args, **kwargs)
