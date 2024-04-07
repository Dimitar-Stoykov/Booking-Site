from django.urls import path

from booking.hotels.views import HotelCreateView

urlpatterns = (
    path('create/', HotelCreateView.as_view(), name='create_hotel'),
)

