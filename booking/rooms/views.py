from django.urls import reverse_lazy
from django.views import generic as views

from booking.rooms.forms import RoomCreateForm


class RoomCreateView(views.CreateView):
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