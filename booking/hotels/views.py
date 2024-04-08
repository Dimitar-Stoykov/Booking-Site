from django.contrib.auth import get_user_model
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


class HotelStaffListView(views.ListView):
    queryset = Hotel.objects.select_related('user').all()
    template_name = 'hotel/list_hotels.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user')


        search_query = self.request.GET.get('search', None)

        if search_query:

            queryset = queryset.filter(
                Q(hotel_name__icontains=search_query) |  # Search by hotel name
                Q(user__email__icontains=search_query)  # Search by user email
            )

        return queryset

