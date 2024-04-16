from django.shortcuts import get_object_or_404

from booking.hotels.models import Hotel


class GetContextMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['check_in_date'] = self.request.GET.get('check_in', '')
        context['check_out_date'] = self.request.GET.get('check_out', '')
        context['adults'] = self.request.GET.get('adults', '')

        hotel_pk = None

        hotel_pk = None

        if hasattr(self, 'kwargs') and 'pk' in self.kwargs:
            hotel_pk = self.kwargs['pk']

        if hotel_pk:
            context['hotel'] = get_object_or_404(Hotel, pk=hotel_pk)

        return context
