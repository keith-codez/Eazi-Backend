from rest_framework import viewsets, status
from .models import BookingRequest
from staff.models import Vehicle, VehicleImage
from .serializers import BookingRequestSerializer, PublicVehicleSerializer, PublicVehicleImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from regulator.permissions import IsCustomer, IsAgent
from rest_framework.exceptions import PermissionDenied
from regulator.models import Agent, Customer



class BookingRequestViewSet(viewsets.ModelViewSet):
    queryset = BookingRequest.objects.select_related('user', 'vehicle').all().order_by('-created_at')
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        # Optionally: show only reviewed/unreviewed based on query param
        queryset = super().get_queryset()
        reviewed = self.request.query_params.get("reviewed")
        if reviewed in ["true", "false"]:
            queryset = queryset.filter(is_reviewed=(reviewed == "true"))
        return queryset
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class PublicVehicleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = PublicVehicleSerializer
    permission_classes = [AllowAny] 
    authentication_classes = [] 

class PublicVehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = PublicVehicleImageSerializer



class StaffBookingRequestViewSet(viewsets.ModelViewSet):
    queryset = BookingRequest.objects.select_related('user', 'vehicle').all()
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAuthenticated, IsAgent]

    def perform_update(self, serializer):
        instance = serializer.save()

        # If status is 'accepted' and agent is authenticated
        if instance.status == 'accepted' and self.request.user.role == 'agent':
            agent = self.request.user.agent_profile  # assumes you have OneToOne User-Agent

            # Attach the agent to the booking request
            instance.agent = agent

            instance.is_reviewed = True
            instance.save()

            
            if not instance.customer:
                instance.customer = customer
                instance.save()

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "agent_profile"):
            return BookingRequest.objects.filter(agent=user.agent_profile).select_related('user', 'vehicle')
        return BookingRequest.objects.none()