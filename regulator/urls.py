from django.urls import path, include
from .views import (
    CustomerRegisterView, AgentRegisterView, AgencyRegisterView, LoginView, CustomerViewSet
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [
  path('register/customer/', CustomerRegisterView.as_view(), name='register-customer'),
  path('register/agent/', AgentRegisterView.as_view(), name='register-agent'),
  path('register/agency/', AgencyRegisterView.as_view(), name='register-agency'),
  path('login/', LoginView.as_view(), name='login'),
  path('', include(router.urls)),
]
