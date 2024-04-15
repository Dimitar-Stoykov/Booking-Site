from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone

UserModel = get_user_model()


class Hotel(models.Model):
    MAX_HOTEL_NAME_LENGTH = 30
    MIN_HOTEL_NAME_LENGTH = 5
    MIN_LOCATION_LENGTH = 10
    MAX_LOCATION_LENGTH = 100

    MOBILE_PHONE_REGEX = RegexValidator(
        regex=r'^\d{9,15}$',
        message="Phone number must be form: 9 Up to 15 digits allowed."
    )

    hotel_name = models.CharField(
        max_length=MAX_HOTEL_NAME_LENGTH,
        validators=[MinLengthValidator(MIN_HOTEL_NAME_LENGTH),],
        unique=True,
    )

    city = models.CharField(
        max_length=40,
    )

    location = models.CharField(
        max_length=MAX_LOCATION_LENGTH,
        validators=[MinLengthValidator(MIN_LOCATION_LENGTH),],
    )

    extra_description = models.TextField()

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
        related_name='hotels',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.hotel_name







