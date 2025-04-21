from django.urls import path, include
from .views import VehicleViewSet, MaintenanceRecordViewSet, VehicleUnavailabilityListCreateView, VehicleCreateView, VehicleImageViewSet, CustomerViewSet, BookingViewSet, StaffBookingRequestViewSet, UserRegistrationView, UserLoginView, UserLogoutView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'maintenance', MaintenanceRecordViewSet)
router.register(r'vehicle-images', VehicleImageViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'booking-requests', StaffBookingRequestViewSet, basename='booking-request')


urlpatterns = [
    path('', include(router.urls)),
    path("vehicle-unavailability/", VehicleUnavailabilityListCreateView.as_view(), name="vehicle-unavailability"),
    path('vehicles/add/', VehicleCreateView.as_view(), name='add-vehicle'),
    path('auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', UserLogoutView.as_view(), name='user-logout'),
    
]
