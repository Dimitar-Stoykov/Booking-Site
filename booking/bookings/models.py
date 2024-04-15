from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from booking.rooms.models import Room

UserModel = get_user_model()


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
