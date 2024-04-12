from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from booking.rooms.forms import RoomCreateForm, RoomPictureUploadForm, ChooseHotelForm
from booking.rooms.mixins import RoomOwnerRequiredMixin



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


class ChooseHotelView(auth_mixins.LoginRequiredMixin, views.FormView):
    template_name = 'rooms/choose_hotel.html'
    form_class = ChooseHotelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

