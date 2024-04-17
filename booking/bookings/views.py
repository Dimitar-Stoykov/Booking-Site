from datetime import datetime

from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic as views

from booking.bookings.forms import BookingForm
from booking.bookings.models import UserBooking
from booking.common.mixins import GetContextMixin
from booking.rooms.models import Room


class CreateBookingView(auth_mixins.LoginRequiredMixin, GetContextMixin, views.CreateView):
    queryset = UserBooking.objects.select_related('room', 'user').all()
    template_name = 'bookings/create_booking.html'
    success_url = reverse_lazy('index_user')
    form_class = BookingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['room'] = self.request.GET.get('room_pk')

        # Extract check-in and check-out dates from the URL parameters
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')

        # Format the dates to exclude time components if they are provided
        if check_in:
            kwargs['check_in'] = datetime.strptime(check_in, '%Y-%m-%d').date()
        if check_out:
            kwargs['check_out'] = datetime.strptime(check_out, '%Y-%m-%d').date()

        kwargs['adults'] = self.request.GET.get('adults')

        if 'check_in' in kwargs and 'check_out' in kwargs and 'room' in kwargs:
            room_obj = Room.objects.get(pk=kwargs['room'])
            price_per_night = room_obj.price_per_night
            delta = (kwargs['check_out'] - kwargs['check_in']).days
            kwargs['cost_of_stay'] = delta * price_per_night

        return kwargs

    def form_valid(self, form):
        # Check if the user has enough money
        if form.is_valid():
            if self.request.user.profile.money >= form.cleaned_data['cost_of_stay']:
                # Withdraw money from the user's profile
                cost_of_stay = form.cleaned_data['cost_of_stay']
                self.request.user.profile.money -= cost_of_stay
                self.request.user.profile.save()

                # Get the room owner and increase their money
                room_owner = form.cleaned_data['room'].hotel.user
                room_owner.profile.money += cost_of_stay
                room_owner.profile.save()

                # Proceed with the booking
                response = super().form_valid(form)
                return response
            else:
                # User doesn't have enough money, show a message and redirect back to the form
                messages.error(self.request, "Not Enough Money you need to deposit")
                return redirect(reverse('create_booking'))
        else:
            return self.form_invalid(form)


class BookingListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = UserBooking
    template_name = 'bookings/booking_list.html'

    def get_queryset(self):
        # Filter UserBooking objects related to the current user
        return UserBooking.objects.select_related('user').filter(user=self.request.user)


class BookingDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = UserBooking

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        cancel_period = self.object.room.hotel.cancel_period
        # Store the cost_of_stay before deleting the booking object
        cost_of_stay = self.object.cost_of_stay
        # Calculate the difference in days between the current date and the booking date
        difference = (self.object.check_in - timezone.now().date()).days
        if difference > cancel_period:
            success_url = self.get_success_url()
            hotel_owner = self.object.room.hotel.user
            hotel_owner.profile.money -= cost_of_stay
            hotel_owner.profile.save()
            user = request.user
            profile = user.profile
            # Increase user's money by the cost_of_stay
            profile.money += cost_of_stay
            profile.save()
            self.object.delete()
            success_message = f'Booking was deleted successfully. Returned money {cost_of_stay}.'
            messages.success(request, success_message)
            # Return the cost_of_stay if deletion is successful
            return HttpResponseRedirect(success_url)
        else:
            error_message = f"Cannot delete the booking as it is less than {cancel_period} days away."
            messages.error(request, error_message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def get_success_url(self):
        return reverse_lazy('booking_details')



