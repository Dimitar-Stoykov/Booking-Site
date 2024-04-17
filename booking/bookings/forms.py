from django import forms
from django.contrib.auth import get_user_model

from booking.bookings.models import UserBooking
from booking.rooms.mixins import ReadOnlyMixin
from booking.rooms.models import Room

UserModel = get_user_model()

class BookingForm(ReadOnlyMixin, forms.ModelForm):
    readonly_fields = ('user', 'room', 'check_in', 'check_out', 'adults', 'cost_of_stay')

    check_in = forms.DateField(label='Check-in Date',
                               widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    check_out = forms.DateField(label='Check-out Date',
                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    adults = forms.IntegerField(label='Number of Adults',
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}))

    def __init__(self, *args, user=None, room=None, check_in=None, check_out=None, adults=None, cost_of_stay=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = user  # Set the initial value for the user field
        self.fields['room'].initial = room  # Set the initial value for the room field

        # Set initial values for check_in, check_out, and adults
        self.fields['check_in'].initial = check_in
        self.fields['check_out'].initial = check_out
        self.fields['adults'].initial = adults
        self.fields['cost_of_stay'].initial = cost_of_stay

        # Restrict queryset for user field to only the pre-filled value
        if user:
            self.fields['user'].queryset = UserModel.objects.filter(pk=user.pk)

        # Restrict queryset for room field to only the pre-filled value
        room_obj = Room.objects.filter(id=room)
        if room_obj:
            self.fields['room'].queryset = Room.objects.filter(pk=room)

    class Meta:
        model = UserBooking
        fields = ('user', 'room', 'check_in', 'check_out', 'adults', 'cost_of_stay')
