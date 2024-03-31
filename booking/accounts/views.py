from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as views

from booking.accounts.forms import BookingUserCreationForm


class BookingRegisterView(views.CreateView):
    template_name = 'accounts/signup.html'
    form_class = BookingUserCreationForm

    def get_success_url(self):
        return reverse_lazy('index')



class BookingLoginView(auth_views.LoginView):
    pass
    # template_name = ''
    # redirect_authenticated_user = True


class ProfileDetailView(views.DetailView):
    pass


class ProfileUpdateView(views.UpdateView):
    pass


class BookingDeleteView(views.DeleteView):
    pass


def sigout(request):
    pass

