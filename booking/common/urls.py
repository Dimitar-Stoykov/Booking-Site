from django.urls import path

from booking.common.views import IndexView, IndexViewUser, AboutView

urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('index/', IndexViewUser.as_view(), name='index_user'),
    path('about/', AboutView.as_view(), name='about'),
)
