from rest_framework import serializers
from .models import BookingRequest
from staff.models import Vehicle, VehicleImage  # For nested data

class VehicleMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'registration_number', 'price_per_day']


class BookingRequestSerializer(serializers.ModelSerializer):
    vehicle = VehicleMiniSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)


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
            'first_name',
            'last_name',
            'phone'
        ]

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

        return BookingRequest.objects.create(
            vehicle=vehicle,
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


