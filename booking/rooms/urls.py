from django.urls import path

from booking.rooms.views import RoomCreateView, PictureUploadView, ChooseHotelView

urlpatterns = (
    path('create/', RoomCreateView.as_view(), name='add_room'),
    path('add/image/<int:pk>/', PictureUploadView.as_view(), name='upload_image'),
    path('hotelchoice/', ChooseHotelView.as_view(), name='choose_hotel'),
)
