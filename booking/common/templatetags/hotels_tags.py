from django import template
from django.db.models import Min, Max

from booking.hotels.models import Hotel

register = template.Library()


@register.filter(name='min_price')
def min_price_filter(hotel):
    if hotel.rooms.exists():
        min_price = hotel.rooms.aggregate(min_price=Min('price_per_night'))
        return min_price['min_price']
    else:
        return 0


@register.filter(name='max_price')
def max_price_filter(hotel):
    if hotel.rooms.exists():
        max_price = hotel.rooms.aggregate(max_price=Max('price_per_night'))
        return max_price['max_price']
    else:
        return