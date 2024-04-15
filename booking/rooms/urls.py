from django.urls import path, include

from booking.rooms.views import RoomCreateView, PictureUploadView, ChooseHotelView, ListRoomView, ChooseHotelListView, \
    RoomDeleteView, RoomUpdateView, PictureListView, PictureDeleteView

urlpatterns = (
    path('create/', RoomCreateView.as_view(), name='add_room'),
    path('<int:pk>/', include([
        path('add/image/', PictureUploadView.as_view(), name='upload_image'),
        path('rooms_list/', ListRoomView.as_view(), name='room_list'),
        path('delete/', RoomDeleteView.as_view(), name='delete_room'),
        path('update/', RoomUpdateView.as_view(), name='update_room'),
        path('pictures/', PictureListView.as_view(), name='room_pictures'),
        path('pictures/delete/', PictureDeleteView.as_view(), name='delete_picture')
    ])),
    path('hotelchoice/', ChooseHotelView.as_view(), name='choose_hotel'),
    path('hotelchoicelist/', ChooseHotelListView.as_view(), name='choose_hotel_list'),

)
