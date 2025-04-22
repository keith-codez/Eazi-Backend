from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, action 
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import VehicleSerializer, MaintenanceRecordSerializer, VehicleUnavailabilitySerializer, VehicleImageSerializer, CustomerSerializer, BookingSerializer, UserSerializer,  StaffBookingRequestSerializer
from .models import Vehicle, MaintenanceRecord, VehicleUnavailability, VehicleImage, Customer, Booking, User
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Sum, F
from rentals.models import BookingRequest
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token as DRFToken
from rest_framework.permissions import IsAuthenticated



class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("DRF is:", DRFToken)
            token, created = DRFToken.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = DRFToken.objects.create(user=user)
            return Response({'token': token.key, 'username': user.username, 'role': user.role})
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = DRFToken.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})




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

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Returns analytics for a specific customer."""
        customer = self.get_object()

        bookings = Booking.objects.filter(customer=customer)

        total_bookings = bookings.count()

        # Correct calculation for total spent
        total_spent = bookings.aggregate(
            total=Sum(F('booking_amount') + F('booking_deposit') - F('discount_amount'))
        )['total'] or 0

        mileage_result = bookings.aggregate(Sum('estimated_mileage'))
        total_mileage = mileage_result.get('estimated_mileage__sum', 0)
        
        return Response({
            "totalBookings": total_bookings,
            "totalSpent": round(total_spent, 2),
            "totalMileage": total_mileage
        })


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer  

    @action(detail=False, methods=['get'], url_path='customer/(?P<customer_id>\\d+)')
    def customer_bookings(self, request, customer_id=None):
        """Returns all bookings for a specific customer."""
        bookings = self.queryset.filter(customer_id=customer_id)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


class StaffBookingRequestViewSet(viewsets.ModelViewSet):
    queryset = BookingRequest.objects.all()
    serializer_class = StaffBookingRequestSerializer
    