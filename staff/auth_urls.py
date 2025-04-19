from django.urls import path
from . import auth_views


urlpatterns = [
    path('customer/register/', auth_views.customer_register),
    path('customer/login/', auth_views.customer_login),
    path('staff/login/', auth_views.staff_login),
    path('me/', auth_views.get_me),
]