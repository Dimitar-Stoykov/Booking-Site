from audioop import reverse

from django import forms
from django.contrib.auth import get_user_model

from booking.hotels.models import Hotel

UserModel = get_user_model()


class HotelBaseForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('hotel_name', 'city', 'location', 'extra_description', 'hotel_picture', 'contact_number', 'user', )


class HotelCreationForm(HotelBaseForm):
    user = forms.ModelChoiceField(queryset=UserModel.objects.all())

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', None)
        super(HotelCreationForm, self).__init__(*args, **kwargs)
        self.fields['hotel_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter hotel name'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter city'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter location'})
        self.fields['extra_description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter hotel amenities'})
        self.fields['hotel_picture'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter hotel picture URL'})
        self.fields['contact_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter contact number'})
        self.fields['user'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Start typing to search for a user', 'id': 'user-search'})


class HotelUpdateForm(HotelBaseForm):

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', None)
        super(HotelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['hotel_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['extra_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['hotel_picture'].widget.attrs.update(
            {'class': 'form-control', })
        self.fields['contact_number'].widget.attrs.update(
            {'class': 'form-control', })
        self.fields['user'].widget.attrs.update(
            {'class': 'form-control'})

