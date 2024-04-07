from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from booking.hotels.forms import HotelCreationForm
from booking.hotels.models import Hotel

UserModel = get_user_model()


class HotelCreateView(views.CreateView):
    model = Hotel
    form_class = HotelCreationForm
    template_name = 'hotel/create_hotel.html'

    def get_success_url(self):
        return reverse_lazy('index_user')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)