from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone

UserModel = get_user_model()


class Hotel(models.Model):
    MAX_HOTEL_NAME_LENGTH = 30
    MIN_HOTEL_NAME_LENGTH = 5
    MOBILE_PHONE_REGEX = RegexValidator(
        regex=r'^\d{9,15}$',
        message="Phone number must be entered in the format: '999999999'. Up to 15 digits allowed."
    )

    hotel_name = models.CharField(
        max_length=MAX_HOTEL_NAME_LENGTH,
        validators=[MinLengthValidator(MIN_HOTEL_NAME_LENGTH),],
        unique=True,
    )

    city = models.CharField(
        max_length=40,
    )

    location = models.TextField()

    hotel_picture = models.URLField()

    contact_number = models.CharField(
        validators=[MOBILE_PHONE_REGEX],
        max_length=15,
        null=False,
        blank=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    created_by = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        related_name='created_hotels',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.hotel_name


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








