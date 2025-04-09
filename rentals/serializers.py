from rest_framework import serializers
from .models import BookingRequest
from staff.models import Vehicle  # For nested data

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

class PublicVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'  # This gives you all model fields