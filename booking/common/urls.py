from django.urls import path

from booking.common.views import IndexView, IndexViewUser

urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('index/', IndexViewUser.as_view(), name='index_user'),
)
