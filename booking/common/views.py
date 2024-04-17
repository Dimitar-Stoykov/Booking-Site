from datetime import datetime

from django.contrib.auth import mixins as auth_mixins
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views import generic as views

from booking.common.mixins import GetContextMixin
from booking.hotels.models import Hotel


class IndexViewUser(auth_mixins.LoginRequiredMixin, GetContextMixin,  views.ListView):
    queryset = Hotel.objects.all().prefetch_related('rooms')
    template_name = 'accounts/index_with_profile.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search', None)
        check_in_date = self.request.GET.get('check_in', None)
        check_out_date = self.request.GET.get('check_out', None)
        adults = self.request.GET.get('adults', None)

        if search_query:
            queryset = queryset.filter(
                Q(hotel_name__icontains=search_query) |
                Q(city__icontains=search_query)
            )

        if adults:
            adults_int = int(adults)
            queryset = queryset.filter(rooms__capacity__gte=adults_int)

        if check_in_date and check_out_date:
            check_in = timezone.datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out = timezone.datetime.strptime(check_out_date, '%Y-%m-%d').date()
            queryset = queryset.filter(
                Q(rooms__booked__isnull=True) |
                Q(rooms__booked__check_in__gt=check_out) |
                Q(rooms__booked__check_out__lte=check_in)
            )

        queryset = queryset.filter(rooms__isnull=False).distinct()

        return queryset


class IndexView(views.TemplateView):
    template_user = 'accounts/index_with_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'index/index.html', {})
        else:
            return render(request, self.template_user)


