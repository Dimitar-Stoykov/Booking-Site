from django.urls import path, include

from booking.rooms.views import RoomCreateView, PictureUploadView, ChooseHotelView, ListRoomView, ChooseHotelListView

urlpatterns = (
    path('create/', RoomCreateView.as_view(), name='add_room'),
    path('<int:pk>/', include([
        path('add/image/', PictureUploadView.as_view(), name='upload_image'),
        path('rooms_list/', ListRoomView.as_view(), name='room_list'),
    ])),
    path('hotelchoice/', ChooseHotelView.as_view(), name='choose_hotel'),
    path('hotelchoicelist/', ChooseHotelListView.as_view(), name='choose_hotel_list'),
    # path('rooms_list/', ListRoomView.as_view(), name='room_list'),

)
