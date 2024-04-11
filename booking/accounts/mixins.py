from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404

UserModel = get_user_model()


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            if hasattr(self, 'get_object'):
                obj_user_pk = self.get_object().pk
            elif hasattr(self, 'object'):
                obj_user_pk = self.object.pk
            else:
                raise AttributeError("OwnerRequiredMixin requires either 'get_object' method or 'object' attribute.")

            user = get_object_or_404(UserModel, pk=obj_user_pk)
        except Http404:
            return redirect('profile_details', pk=request.user.pk)

        if obj_user_pk != request.user.pk:
            return redirect('profile_details', pk=request.user.pk)

        return super().dispatch(request, *args, **kwargs)
