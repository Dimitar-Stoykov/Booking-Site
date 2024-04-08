from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic as views

from booking.hotels.forms import HotelCreationForm, RoomCreateForm
from booking.hotels.mixins import StaffRequiredMixin
from booking.hotels.models import Hotel

UserModel = get_user_model()


class HotelCreateView(StaffRequiredMixin, views.CreateView):
    model = Hotel
    form_class = HotelCreationForm
    template_name = 'hotel/create_hotel.html'

    def get_success_url(self):
        return reverse_lazy('index_user')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RoomCreateView(views.CreateView):
    template_name = 'hotel/add_room.html'
    form_class = RoomCreateForm
    # TODO: redirect to created room ?
    def get_success_url(self):
        return reverse_lazy('index_user')
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs