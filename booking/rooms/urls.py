from django.urls import path

from booking.rooms.views import RoomCreateView

urlpatterns = (
    path('create/', RoomCreateView.as_view(), name='add_room'),
)