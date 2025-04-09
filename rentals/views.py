from rest_framework import viewsets
from .models import BookingRequest
from staff.models import Vehicle
from .serializers import BookingRequestSerializer, PublicVehicleSerializer

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