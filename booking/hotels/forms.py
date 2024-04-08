from audioop import reverse

from django import forms
from django.contrib.auth import get_user_model

from booking.hotels.models import Hotel, Room

UserModel = get_user_model()


class HotelCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=UserModel.objects.all())

    class Meta:
        model = Hotel
        fields = ('hotel_name', 'city', 'location', 'hotel_picture', 'contact_number', 'user')

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', None)
        super(HotelCreationForm, self).__init__(*args, **kwargs)
        self.fields['hotel_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter hotel name'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter city'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter location'})
        self.fields['hotel_picture'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter hotel picture URL'})
        self.fields['contact_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter contact number'})
        self.fields['user'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Start typing to search for a user', 'id': 'user-search'})


class RoomCreateForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super(RoomCreateForm, self).__init__(*args, **kwargs)
        self.fields['hotel'].queryset = Hotel.objects.filter(user=self.user)

    hotel = forms.ModelChoiceField(queryset=Hotel.objects.none(), widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Select a hotel'}))

    class Meta:
        model = Room
        fields = ('room_number', 'price_per_night', 'capacity', 'hotel',)
        widgets = {
            'room_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter room number'}),
            'price_per_night': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter price per night'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        room_number = cleaned_data.get("room_number")
        hotel = cleaned_data.get("hotel")

        if Room.objects.filter(hotel=hotel, room_number=room_number).exists():
            self.add_error(None, 'A room with this number already exists for this hotel.')

        return cleaned_data