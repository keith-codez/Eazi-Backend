from django.urls import path, include
from .views import (
    CustomerRegisterView, AgentRegisterView, AgencyRegisterView, LoginView, CustomerViewSet
)
from rest_framework.routers import DefaultRouter
from staff.views import (
    VehicleViewSet,
    MaintenanceRecordViewSet,
    VehicleImageViewSet,
    BookingViewSet,
    StaffBookingRequestViewSet
)
from rentals.views import PublicVehicleViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r"staff-vehicles", VehicleViewSet, basename="vehicle")
router.register(r"vehicle-images", VehicleImageViewSet, basename="vehicle-image")
router.register(r"maintenance", MaintenanceRecordViewSet, basename="maintenance")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"booking-requests", StaffBookingRequestViewSet, basename="booking-request")
router.register(r"public-vehicles", PublicVehicleViewSet, basename="public-vehicles")


urlpatterns = [
  path('register/customer/', CustomerRegisterView.as_view(), name='register-customer'),
  path('register/agent/', AgentRegisterView.as_view(), name='register-agent'),
  path('register/agency/', AgencyRegisterView.as_view(), name='register-agency'),
  path('login/', LoginView.as_view(), name='login'),
  path('', include(router.urls)),
  path('regulator/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('regulator/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
