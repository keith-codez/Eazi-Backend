from django.urls import path, include
from .views import register_manager, login_manager
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", register_manager, name="register_manager"),
    path("login/", login_manager, name="login_manager"),
    path('auth/', include('djoser.urls')),  # Includes authentication routes (including password reset)
    path('auth/', include('djoser.urls.authtoken')),  # Includes token-based authentication routes
]
