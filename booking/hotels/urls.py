from django.urls import path, include

from booking.hotels.views import HotelCreateView, HotelStaffListView

urlpatterns = (
    path('create/', HotelCreateView.as_view(), name='create_hotel'),
    path('update/', HotelStaffListView.as_view(), name='list_hotel')

)

