from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, BookingViewSet

router= DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'bookings', BookingViewSet)


urlpatterns = [
    path('', include(router.urls)), 
]