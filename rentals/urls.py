from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingRequestViewSet, PublicVehicleViewSet, register_customer, login_customer




router= DefaultRouter()
router.register(r'booking-requests', BookingRequestViewSet, basename='booking-request'), 
router.register(r"vehicles", PublicVehicleViewSet, basename="public-vehicles")

urlpatterns = [
    path('', include(router.urls)), 
    path("auth/register/customer/", register_customer, name="register_customer"),
    path("auth/login/customer/", login_customer, name="login_customer"),
]