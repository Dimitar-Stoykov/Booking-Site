from django.contrib.auth import mixins as auth_mixins
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from booking.hotels.models import Hotel
from booking.rooms.models import Room


class HotelOwnerRequiredMixin(auth_mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('pk')

        if not request.user.hotel_set.filter(id=hotel_id).exists():
            return redirect('add_room')

        return super().dispatch(request, *args, **kwargs)


class DispatchHotelIdMixin:
    hotel_id = None

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        self.hotel_id = obj.hotel_id
        return obj

    def dispatch(self, request, *args, **kwargs):
        try:
            room_obj = self.get_object()
            hotel_id = room_obj.hotel_id

            if not request.user.hotel_set.filter(id=hotel_id).exists():
                # Redirect to 'add_room' if user's hotel does not match the room's hotel
                return redirect('add_room')
        except Http404:
            # Redirect to 'add_room' if room is not found
            return redirect('add_room')

        return super().dispatch(request, *args, **kwargs)


class ReadOnlyMixin:
    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.readonly_fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs['readonly'] = 'readonly'


class RoomOwnerRequiredMixin(auth_mixins.LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        room_id = self.kwargs.get('pk')

        room = Room.objects.filter(id=room_id).first()

        if not room or (room.hotel.user != request.user):
            return redirect(reverse('add_room'))

        return super().dispatch(request, *args, **kwargs)

