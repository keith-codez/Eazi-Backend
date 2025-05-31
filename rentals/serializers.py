from rest_framework import serializers
from .models import BookingRequest
from staff.models import Vehicle, VehicleImage  # For nested data
from regulator.serializers import CustomerMiniSerializer, CustomerSerializer
from regulator.models import Customer
from rest_framework.exceptions import NotAuthenticated


class VehicleMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'registration_number', 'price_per_day']


class BookingRequestSerializer(serializers.ModelSerializer):
    vehicle = VehicleMiniSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True)
    customer = serializers.SerializerMethodField()


    class Meta:
        model = BookingRequest
        fields = [
            'id',
            'vehicle',
            'vehicle_id',
            'start_date',
            'end_date',
            'message',
            'is_reviewed',
            'status',
            'staff_notes',
            'customer'
        ]


    def create(self, validated_data):
        request = self.context.get('request')
        
        if not request or not request.user or not request.user.is_authenticated:
            raise NotAuthenticated("You must be logged in as a customer to submit a booking request.")

        user = request.user
        customer = getattr(user, 'customer_profile', None)

        if not customer:
            raise serializers.ValidationError("Booking requests must come from a registered customer.")

        vehicle = validated_data.pop('vehicle_id')

        return BookingRequest.objects.create(
            user=user,
            customer=customer,
            vehicle=vehicle,
            **validated_data
        )

    def get_customer(self, obj):
        user = obj.user
        try:
            customer = user.customer_profile
            return {
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone_number": customer.phone_number,
            }
        except Customer.DoesNotExist:
            return None

class PublicVehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ["id", "image"]
        extra_kwargs = {
            "image": {"use_url": True}  # This ensures the URL is included in the response
        }

class PublicVehicleSerializer(serializers.ModelSerializer):

    images = PublicVehicleImageSerializer(many=True, read_only=True)  # Include images in the vehicle serializer
    class Meta:
        model = Vehicle
        fields = '__all__'  # This gives you all model fields


