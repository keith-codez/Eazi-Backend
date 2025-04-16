from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingRequestViewSet, PublicVehicleViewSet




router= DefaultRouter()
router.register(r'booking-requests', BookingRequestViewSet, basename='booking-request'), 
router.register(r"vehicles", PublicVehicleViewSet, basename="public-vehicles")

urlpatterns = [
    path('', include(router.urls)), 
]