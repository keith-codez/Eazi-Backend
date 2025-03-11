from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vehicle, VehicleImage, MaintenanceRecord, VehicleUnavailability



User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ["id", "image"]
        extra_kwargs = {
            "image": {"use_url": True}  # This ensures the URL is included in the response
        }

class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    image_uploads = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    removed_images = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Vehicle
        fields = ["id", "make", "model", "manufacture_year", "color", "mileage", "mileage_allowance", "ownership", "price_per_day", "deposit", "maintenance_records", "registration_number", "next_service_date", "images", "image_uploads", "removed_images"]

    def update(self, instance, validated_data):
        images_data = validated_data.pop("image_uploads", None)
        removed_images = validated_data.pop("removed_images", [])

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle new image uploads
        if images_data:
            for image_data in images_data:
                VehicleImage.objects.create(vehicle=instance, image=image_data)

        # Remove deleted images
        if removed_images:
            VehicleImage.objects.filter(id__in=removed_images).delete()

        return instance


class VehicleUnavailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleUnavailability
        fields = ["id", "vehicle", "start_date", "end_date", "reason"]