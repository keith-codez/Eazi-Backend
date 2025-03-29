from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, action 
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, VehicleSerializer, MaintenanceRecordSerializer, VehicleUnavailabilitySerializer, VehicleImageSerializer, CustomerSerializer
from .models import Vehicle, MaintenanceRecord, VehicleUnavailability, VehicleImage, Customer
from rest_framework.parsers import MultiPartParser, FormParser




User = get_user_model()

@api_view(["POST"])
def register_manager(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_manager(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)





class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = (MultiPartParser, FormParser)  # ✅ Allow image uploads

    def update(self, request, *args, **kwargs):
        vehicle = self.get_object()
        serializer = self.get_serializer(vehicle, data=request.data, partial=True)

        if serializer.is_valid():
            vehicle = serializer.save()

            # ✅ Handle image deletion
            deleted_images = request.data.get("deleted_images")
            if deleted_images:
                image_ids = eval(deleted_images)  # Convert string to list
                VehicleImage.objects.filter(id__in=image_ids).delete()

            # ✅ Handle new images
            if "images" in request.FILES:
                for img in request.FILES.getlist("images"):
                    VehicleImage.objects.create(vehicle=vehicle, image=img)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer


class VehicleUnavailabilityListCreateView(generics.ListCreateAPIView):
    queryset = VehicleUnavailability.objects.all()
    serializer_class = VehicleUnavailabilitySerializer



class VehicleCreateView(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def update(self, request, *args, **kwargs):
        """Handles updating customer, including driver's license file handling"""
        customer = self.get_object()

        # Check if frontend sent a DELETE request for the driver's license
        if request.data.get("drivers_license") == "DELETE":
            customer.delete_drivers_license()

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['DELETE'])
    def delete_drivers_license(self, request, pk=None):
        """Deletes only the driver's license image"""
        customer = self.get_object()
        customer.delete_drivers_license()
        return Response({"message": "Driver's license deleted successfully"}, status=status.HTTP_204_NO_CONTENT)