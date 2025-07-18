from django.urls import path, include
from .views import VehicleViewSet, MaintenanceRecordViewSet, VehicleUnavailabilityListCreateView, VehicleCreateView, VehicleImageViewSet, BookingViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'maintenance', MaintenanceRecordViewSet)
router.register(r'vehicle-images', VehicleImageViewSet)
router.register(r'bookings', BookingViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path("vehicle-unavailability/", VehicleUnavailabilityListCreateView.as_view(), name="vehicle-unavailability"),
    path('vehicles/add/', VehicleCreateView.as_view(), name='add-vehicle'),
]
