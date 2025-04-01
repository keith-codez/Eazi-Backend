from django.urls import path, include
from .views import register_manager, login_manager, VehicleViewSet, MaintenanceRecordViewSet, VehicleUnavailabilityListCreateView, VehicleCreateView, VehicleImageViewSet, CustomerViewSet, BookingViewSet
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'maintenance', MaintenanceRecordViewSet)
router.register(r'vehicle-images', VehicleImageViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'bookings', BookingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("register/", register_manager, name="register_manager"),
    path("login/", login_manager, name="login_manager"),
    path('auth/', include('djoser.urls')),  # Includes authentication routes (including password reset)
    path('auth/', include('djoser.urls.authtoken')),  # Includes token-based authentication routes
    path("vehicle-unavailability/", VehicleUnavailabilityListCreateView.as_view(), name="vehicle-unavailability"),
    path('vehicles/add/', VehicleCreateView.as_view(), name='add-vehicle'),
    
]
