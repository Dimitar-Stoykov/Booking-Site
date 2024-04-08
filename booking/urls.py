from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.common.urls')),
    path('accounts/', include('booking.accounts.urls')),
    path('booking/', include('booking.bookings.urls')),
    path('hotels/', include('booking.hotels.urls')),
    path('rooms/', include('booking.rooms.urls')),
]
