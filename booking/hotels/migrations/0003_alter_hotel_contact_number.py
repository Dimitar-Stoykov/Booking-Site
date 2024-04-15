# Generated by Django 4.2.11 on 2024-04-15 13:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_remove_roompictures_room_hotel_contact_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='contact_number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number must be form: 9 Up to 15 digits allowed.', regex='^\\d{9,15}$')]),
        ),
    ]
