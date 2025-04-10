from rest_framework import serializers
from .models import BookingRequest, CustomerUser
from staff.models import Vehicle, VehicleImage  # For nested data

class VehicleMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'registration_number', 'price_per_day']

class BookingRequestSerializer(serializers.ModelSerializer):
    vehicle = VehicleMiniSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True)

    class Meta:
        model = BookingRequest
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'start_date', 'end_date', 'message', 'vehicle', 'vehicle_id', 'is_reviewed', 'created_at']
        read_only_fields = ['is_reviewed', 'created_at']

    def create(self, validated_data):
        vehicle = validated_data.pop('vehicle_id')
        return BookingRequest.objects.create(vehicle=vehicle, **validated_data)

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


class CustomerRegisterSerializer(serializers.ModelSerializer):
    # We expect the registration form to include these extra fields:
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomerUser
        fields = ['email', 'username', 'phone_number', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # Extract first and last names which are not part of CustomerUser model
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        # Use our custom manager to create the customer user and the associated Customer profile
        user = CustomerUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            **validated_data
        )
        return user

class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()