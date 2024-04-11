from django.urls import path, include

from booking.hotels.views import HotelCreateView, HotelStaffListView, HotelDeleteView, HotelUpdateView

urlpatterns = (
    path('create/', HotelCreateView.as_view(), name='create_hotel'),
    path('update/', HotelStaffListView.as_view(), name='list_hotel'),
    path('<int:pk>/', include([
        path('delete/', HotelDeleteView.as_view(), name='delete_hotel'),
        path('update/', HotelUpdateView.as_view(), name='update_hotel'),
    ])),

)

