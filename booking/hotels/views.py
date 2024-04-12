from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import mixins as auth_mixins
from django.db.models import Q

from django.urls import reverse_lazy
from django.views import generic as views

from booking.hotels.forms import HotelCreationForm, HotelUpdateForm
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


class HotelStaffListView(StaffRequiredMixin, views.ListView):
    queryset = Hotel.objects.select_related('user').all()
    template_name = 'hotel/list_hotels.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search', None)

        if search_query:

            queryset = queryset.filter(
                Q(hotel_name__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )

        return queryset


class HotelDetailView(auth_mixins.LoginRequiredMixin, views.ListView):
    pass
    #TODO: show rooms and extra_description


class HotelUpdateView(StaffRequiredMixin, views.UpdateView):
    template_name = 'hotel/update_hotel.html'
    queryset = Hotel.objects.all().select_related('user')
    form_class = HotelUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the form with the instance data to the template
        context['form'] = HotelUpdateForm(instance=self.get_object())
        return context

    def get_success_url(self):

        return reverse_lazy('list_hotel')


class HotelDeleteView(StaffRequiredMixin, views.DeleteView):
    model = Hotel

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        hotel = self.object
        success_message = f'Hotel "{hotel.hotel_name}" was deleted successfully.'
        messages.success(request, success_message)
        return response

    def get_success_url(self):
        return reverse_lazy('list_hotel')

