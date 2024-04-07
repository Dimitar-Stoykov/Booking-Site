from django.contrib import messages
from django.contrib.auth import views as auth_views, logout, update_session_auth_hash
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django import forms
from booking.accounts.forms import BookingUserCreationForm, CustomPasswordChangeForm
from booking.accounts.mixins import OwnerRequiredMixin
from booking.accounts.models import Profile


class BookingRegisterView(views.CreateView):
    template_name = 'accounts/signup.html'
    form_class = BookingUserCreationForm

    def get_success_url(self):
        return reverse_lazy('index')


class BookingLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'date_of_birth', 'money')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ProfileUpdateView(OwnerRequiredMixin, views.UpdateView):
    queryset = Profile.objects.prefetch_related('user').all()
    template_name = 'accounts/profile_details.html'
    # fields = ('first_name', 'last_name', 'date_of_birth', 'money')
    # widgets = {
    #     'date_of_birth': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}),
    # }

    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})


class ProfilePasswordUpdateView(auth_views.PasswordChangeView):
    template_name = 'accounts/profile_password.html'
    form_class = CustomPasswordChangeForm

    def get_success_url(self):
        # Redirect to the same page
        return self.request.path

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Your password has been changed successfully.')
        return HttpResponseRedirect(self.get_success_url())


class BookingDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    pass


@login_required
def signout(request):
    logout(request)

    return redirect('index')

