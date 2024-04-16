from abc import ABC, abstractmethod

from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views


from booking.rooms.forms import RoomCreateForm, RoomPictureUploadForm, ChooseHotelForm, RoomUpdateForm
from booking.rooms.mixins import HotelOwnerRequiredMixin, RoomOwnerRequiredMixin, DispatchHotelIdMixin
from booking.rooms.models import Room, RoomPictures


class RoomCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'rooms/add_room.html'
    form_class = RoomCreateForm

    def get_success_url(self):
        return reverse_lazy('add_room')

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


class ChooseHotelListView(ChooseHotelBaseView):
    template_name = 'rooms/choose_hotel_list_room.html'

    def form_valid(self, form):
        selected_hotel_id = form.cleaned_data['hotel'].id
        return redirect(reverse('room_list', kwargs={'pk': selected_hotel_id}))


class ListRoomView(HotelOwnerRequiredMixin, views.ListView):
    template_name = 'rooms/rooms_list.html'

    def get_queryset(self):
        hotel_id = self.kwargs.get('pk')
        search_query = self.request.GET.get('search')

        if search_query:
            rooms = Room.objects.select_related('hotel').prefetch_related('hotel__user').filter(
                Q(hotel__user=self.request.user),
                Q(hotel_id=hotel_id),
                Q(room_number__icontains=search_query),
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


class RoomUpdateView(auth_mixins.LoginRequiredMixin, DispatchHotelIdMixin, views.UpdateView):
    template_name = 'rooms/update_room.html'
    queryset = Room.objects.select_related('hotel').all()
    form_class = RoomUpdateForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Room {self.object} was updated successfully.")

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the form with the instance data to the template
        context['form'] = RoomUpdateForm(instance=self.get_object())
        return context

    def get_success_url(self):
        return reverse_lazy('room_list', kwargs={'pk': self.hotel_id})


class RoomDeleteView(auth_mixins.LoginRequiredMixin, DispatchHotelIdMixin, views.DeleteView):
    model = Room

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        success_message = f'Room "{self.object.room_number}" was deleted successfully.'
        messages.success(request, success_message)
        return response

    def get_success_url(self):
        return reverse_lazy('room_list', kwargs={'pk': self.hotel_id})


class PictureUploadView(HotelOwnerRequiredMixin, views.CreateView):
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
        instance = form.save(commit=False)
        instance.room_id = form.cleaned_data['room'].id

        instance.save()
        return redirect(reverse('upload_image', kwargs={'pk': instance.room.hotel_id}))


class PictureListView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = 'rooms/pictures_room_list.html'
    paginate_by = 1

    def get_queryset(self):
        room_id = self.kwargs.get('pk')

        query = RoomPictures.objects.select_related('room').filter(room_id=room_id)

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = self.kwargs.get('pk')
        room = Room.objects.filter(id=room_id).first()
        if room:
            context['hotel_id'] = room.hotel_id
            context['is_owner'] = room.hotel.user == self.request.user
        else:
            context['is_owner'] = False

        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.request.path_info)


class PictureDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = RoomPictures

    def get_success_url(self):
        # Get the room_id before deletion
        deleted_object = self.get_object()
        room_id = deleted_object.room_id

        # Redirect to the room after deletion
        return reverse_lazy('room_pictures', kwargs={'pk': room_id})

    def dispatch(self, request, *args, **kwargs):

        picture = self.get_object()

        if request.user != picture.room.hotel.user:
            return redirect('add_room')
        
        return super().dispatch(request, *args, **kwargs)