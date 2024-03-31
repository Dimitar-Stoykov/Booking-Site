
from django.contrib.auth import views as auth_views, logout
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from booking.accounts.forms import BookingUserCreationForm
from booking.accounts.models import Profile


class BookingRegisterView(views.CreateView):
    template_name = 'accounts/signup.html'
    form_class = BookingUserCreationForm

    def get_success_url(self):
        return reverse_lazy('index')


class BookingLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class ProfileDetailView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    queryset = Profile.objects.prefetch_related('user').all()
    template_name = 'accounts/profile_details.html'
    fields = ('first_name', 'last_name', 'date_of_birth', 'money')

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})


class ProfileUpdateView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    pass


class BookingDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    pass


@login_required
def signout(request):
    logout(request)

    return redirect('index')

