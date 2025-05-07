from rest_framework import viewsets, status
from .models import BookingRequest, Lead
from staff.models import Vehicle, VehicleImage
from .serializers import BookingRequestSerializer, PublicVehicleSerializer, PublicVehicleImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny


class BookingRequestViewSet(viewsets.ModelViewSet):
    queryset = BookingRequest.objects.all().order_by('-created_at')
    serializer_class = BookingRequestSerializer
    permission_classes = []

    def get_queryset(self):
        # Optionally: show only reviewed/unreviewed based on query param
        queryset = super().get_queryset()
        reviewed = self.request.query_params.get("reviewed")
        if reviewed in ["true", "false"]:
            queryset = queryset.filter(is_reviewed=(reviewed == "true"))
        return queryset


class PublicVehicleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = PublicVehicleSerializer
    permission_classes = [AllowAny] 
    authentication_classes = [] 

class PublicVehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = PublicVehicleImageSerializer



