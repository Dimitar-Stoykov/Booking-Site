from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from booking.rooms.models import Room

UserModel = get_user_model()


class UserBooking(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='booked'

    )

    check_in = models.DateField()

    check_out = models.DateField()

    adults = models.PositiveIntegerField()

    cost_of_stay = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1),],
    )

    def save(self, *args, **kwargs):

        if UserBooking.objects.filter(room=self.room, check_in__lte=self.check_out, check_out__gt=self.check_in).exists():
            # If the room is already booked for any overlapping period, raise ValidationError
            raise ValidationError('This room is already booked for the specified period.')
        # If the room is available, save the Booking instance
        super().save(*args, **kwargs)
