from django.urls import path, include

from booking.hotels.views import HotelCreateView, RoomCreateView

urlpatterns = (
    path('create/', HotelCreateView.as_view(), name='create_hotel'),

    path('rooms/', include([
     path('create/', RoomCreateView.as_view(), name='add_room'),
    ]))
)

