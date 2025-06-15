from rest_framework import viewsets, status
from .models import BookingRequest
from staff.models import Vehicle, VehicleImage
from .serializers import BookingRequestSerializer, PublicVehicleSerializer, PublicVehicleImageSerializer, StaffBookingRequestUpdateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from regulator.permissions import IsCustomer, IsAgent, IsOwnerOfBookingRequest
from rest_framework.exceptions import PermissionDenied
from regulator.models import Agent, Customer



class BookingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAuthenticated, IsCustomer, IsOwnerOfBookingRequest]

    def get_queryset(self):
        # Only return booking requests for the logged-in customer
        user = self.request.user
        return BookingRequest.objects.select_related('user', 'vehicle')\
            .filter(user=user)\
            .order_by('-created_at')
    

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
        # Get the previous state of the instance before saving
        instance = serializer.instance
        previous_status = instance.status

        # Save the updated instance
        instance = serializer.save()

        # If the status changed from 'pending' to either 'accepted' or 'declined'
        if previous_status == 'pending' and instance.status in ['accepted', 'declined']:
            instance.is_reviewed = True

            # If accepted and agent is authenticated, assign agent
            if instance.status == 'accepted' and self.request.user.role == 'agent':
                agent = self.request.user.agent_profile  # assumes you have OneToOne User-Agent
                instance.agent = agent

            instance.save()


    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "agent_profile"):
            return BookingRequest.objects.filter(agent=user.agent_profile).select_related('user', 'vehicle')
        return BookingRequest.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return StaffBookingRequestUpdateSerializer
        return BookingRequestSerializer