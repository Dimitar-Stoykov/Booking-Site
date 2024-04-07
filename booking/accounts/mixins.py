from django.shortcuts import redirect


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if hasattr(self, 'get_object'):
            obj_user_pk = self.get_object().pk
        elif hasattr(self, 'object'):
            obj_user_pk = self.object.pk
        else:
            raise AttributeError("OwnerRequiredMixin requires either 'get_object' method or 'object' attribute.")

        if obj_user_pk != request.user.pk:
            return redirect('profile_details', pk=request.user.pk)

        return super().dispatch(request, *args, **kwargs)
