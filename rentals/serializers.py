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

    lead = LeadSerializer(read_only=True)  # still useful to expose lead details if needed

    class Meta:
        model = BookingRequest
        fields = [
            'id',
            'start_date', 'end_date', 'message',
            'vehicle', 'vehicle_id',
            'lead',
            'is_reviewed', 'created_at'
        ]
        read_only_fields = ['is_reviewed', 'created_at']

    def create(self, validated_data):
        request = self.context['request']
        vehicle = validated_data.pop('vehicle_id')

        # Optional: infer lead from logged-in customer
        user = request.user
        customer = getattr(user, 'customer', None)

        if not customer:
            raise serializers.ValidationError("Booking requests must come from a registered customer.")

        # Option 1: link directly to customer (if lead model is removed)
        # Option 2: create a Lead object if keeping it as intermediate

        lead = Lead.objects.create(
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            phone_number=customer.phone_number
        )

        return BookingRequest.objects.create(
            vehicle=vehicle,
            lead=lead,
            **validated_data
        )



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


