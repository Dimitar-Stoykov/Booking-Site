from django.shortcuts import redirect


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        obj_user_pk = self.get_object().user.pk
        if obj_user_pk != request.user.pk:
            return redirect('profile_details', pk=request.user.pk)

        return super().dispatch(request, *args, **kwargs)
