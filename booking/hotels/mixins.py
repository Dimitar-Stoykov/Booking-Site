from django.shortcuts import redirect


class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:

            return redirect('login')

        if not request.user.is_superuser or not request.user.is_staff:

            return redirect('index_user')


        return super().dispatch(request, *args, **kwargs)