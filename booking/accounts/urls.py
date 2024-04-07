from django.urls import path, include

from booking.accounts.views import BookingRegisterView, BookingLoginView, signout, ProfileUpdateView, \
    ProfilePasswordUpdateView, BookingDeleteView

urlpatterns = (
    path('register/', BookingRegisterView.as_view(), name='signup'),
    path('login/', BookingLoginView.as_view(), name='login'),
    path('logout/', signout, name='signout'),
    path('profile/<int:pk>/', include([
        path('', ProfileUpdateView.as_view(), name='profile_details'),
        path('password/', ProfilePasswordUpdateView.as_view(), name='password_change'),
        path('delete/', BookingDeleteView.as_view(), name='delete_profile'),
    ])),
)