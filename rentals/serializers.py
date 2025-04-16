from rest_framework import serializers
from .models import BookingRequest, Lead
from staff.models import Vehicle, VehicleImage  # For nested data

class VehicleMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'registration_number', 'price_per_day']



class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'phone_number']




class BookingRequestSerializer(serializers.ModelSerializer):
    vehicle = VehicleMiniSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True)

    # New nested field
    lead = LeadSerializer(read_only=True)

    # Fields for lead creation
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = BookingRequest
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'start_date', 'end_date', 'message',
            'vehicle', 'vehicle_id', 'lead',  # Include lead
            'is_reviewed', 'created_at'
        ]
        read_only_fields = ['is_reviewed', 'created_at']

    def create(self, validated_data):
        vehicle = validated_data.pop('vehicle_id')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        phone_number = validated_data.pop('phone_number')

        # Create a new Lead
        lead = Lead.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )

        # Create the booking request with the lead
        return BookingRequest.objects.create(vehicle=vehicle, lead=lead, **validated_data)



    def __str__(self):
        if self.lead:
            return f"{self.lead.first_name} {self.lead.last_name} - {self.vehicle}"
        return f"Booking Request - {self.vehicle}"


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


