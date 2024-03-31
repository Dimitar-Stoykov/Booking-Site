from django.urls import path, include

from booking.accounts.views import BookingRegisterView, BookingLoginView, signout, ProfileDetailView

urlpatterns = (
    path('register/', BookingRegisterView.as_view(), name='signup'),
    path('login/', BookingLoginView.as_view(), name='login'),
    path('logout/', signout, name='signout'),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailView.as_view(), name='profile_details'),
    ])),
)