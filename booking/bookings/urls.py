from django.urls import path

from booking.bookings.views import CreateBookingView, BookingListView, BookingDeleteView

urlpatterns = (
    path('create/', CreateBookingView.as_view(), name='create_booking'),
    path('details/', BookingListView.as_view(), name='booking_details'),
    path('delete/<int:pk>/', BookingDeleteView.as_view(), name='delete_booking'),
)
