from abc import ABC, abstractmethod

from django.contrib.auth import mixins as auth_mixins
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from booking.hotels.models import Hotel
from booking.rooms.forms import RoomCreateForm, RoomPictureUploadForm, ChooseHotelForm
from booking.rooms.mixins import RoomOwnerRequiredMixin
from booking.rooms.models import Room


class RoomCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'rooms/add_room.html'
    form_class = RoomCreateForm
    # TODO: redirect to created room ?

    def get_success_url(self):
        return reverse_lazy('index_user')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ChooseHotelBaseView(ABC, auth_mixins.LoginRequiredMixin, views.FormView):
    template_name = ''
    form_class = ChooseHotelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    @abstractmethod
    def form_valid(self, form):
        pass


class ChooseHotelView(ChooseHotelBaseView):
    template_name = 'rooms/choose_hotel.html'

    def form_valid(self, form):
        selected_hotel_id = form.cleaned_data['hotel'].id
        return redirect(reverse('upload_image', kwargs={'pk': selected_hotel_id}))


class PictureUploadView(auth_mixins.LoginRequiredMixin, RoomOwnerRequiredMixin, views.CreateView):
    template_name = 'rooms/add_room_img.html'
    form_class = RoomPictureUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel_id'] = self.kwargs.get('pk')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        hotel_id = self.kwargs.get('pk')
        kwargs['hotel_id'] = hotel_id
        return kwargs

    def form_valid(self, form):
        # Save the form and redirect to success URL
        instance = form.save(commit=False)
        instance.room_id = form.cleaned_data['room'].id
        instance.save()
        return redirect(reverse('upload_image', kwargs={'pk': instance.room.hotel_id}))


class ChooseHotelListView(ChooseHotelBaseView):
    template_name = 'rooms/choose_hotel_list_room.html'

    def form_valid(self, form):
        selected_hotel_id = form.cleaned_data['hotel'].id
        return redirect(reverse('room_list', kwargs={'pk': selected_hotel_id}))


class ListRoomView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = 'rooms/rooms_list.html'

    def get_queryset(self):
        hotel_id = self.kwargs.get('pk')
        search_query = self.request.GET.get('search')

        if search_query:
            rooms = Room.objects.select_related('hotel').prefetch_related('hotel__user').filter(
                Q(hotel__user=self.request.user),
                Q(hotel_id=hotel_id),
                Q(room_number__icontains=search_query)
            )
        else:
            rooms = Room.objects.select_related('hotel').prefetch_related('hotel__user').filter(
                Q(hotel__user=self.request.user),
                Q(hotel_id=hotel_id)
            )

        return rooms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel_id'] = self.kwargs.get('pk')
        return context

