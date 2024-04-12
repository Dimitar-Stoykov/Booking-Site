from django.shortcuts import redirect


class RoomOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('pk')

        if not request.user.hotel_set.filter(id=hotel_id).exists():
            return redirect('choose_hotel')

        return super().dispatch(request, *args, **kwargs)