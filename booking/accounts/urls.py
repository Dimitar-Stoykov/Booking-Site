from django.urls import path

from booking.accounts.views import BookingRegisterView

urlpatterns = (
    path('register/', BookingRegisterView.as_view(), name='signup'),
)