from rest_framework import viewsets, status
from .models import BookingRequest, CustomerUser
from staff.models import Vehicle, VehicleImage
from .serializers import BookingRequestSerializer, PublicVehicleSerializer, PublicVehicleImageSerializer, CustomerRegisterSerializer, CustomerLoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


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

class PublicVehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = PublicVehicleImageSerializer



@api_view(["POST"])
def register_customer(request):
    serializer = CustomerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Customer registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def login_customer(request):
    serializer = CustomerLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        try:
            user = CustomerUser.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "message": "Customer login successful"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomerUser.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)