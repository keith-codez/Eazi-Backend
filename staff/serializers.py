from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vehicle, VehicleImage, MaintenanceRecord, VehicleUnavailability, Booking, Location
from rentals.models import BookingRequest
from regulator.models import Customer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'city', 'address']


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

    agent = serializers.PrimaryKeyRelatedField(read_only=True)
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

    pickup_locations = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Location.objects.all(),
        required=False
    )

    class Meta:
        model = Vehicle
        fields = ["id", "agent", "make", "model", "manufacture_year", "color", "mileage", "mileage_allowance", "ownership", 
                  "price_per_day", "deposit", "maintenance_records", "registration_number", "next_service_date", 
                  "images", "image_uploads", "removed_images",  "pickup_locations"]

    def create(self, validated_data):
        """ Handles creating a vehicle along with image uploads. """
        images_data = validated_data.pop("image_uploads", [])  # Extract image data before creation
        pickup_locations = validated_data.pop("pickup_locations", [])

        
        vehicle = Vehicle.objects.create(**validated_data)  # Create vehicle
        
        vehicle.pickup_locations.set(pickup_locations)
        
        # Handle image uploads
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=vehicle, image=image_data)
        
        return vehicle

    def update(self, instance, validated_data):
        """ Handles updating a vehicle, including adding/removing images. """
        images_data = validated_data.pop("image_uploads", [])  # Extract images
        removed_images = validated_data.pop("removed_images", [])  # Extract IDs of images to remove

        # Update vehicle fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle new image uploads
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=instance, image=image_data)

        # Handle image deletions
        if removed_images:
            VehicleImage.objects.filter(id__in=removed_images, vehicle=instance).delete()

        return instance


class VehicleUnavailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleUnavailability
        fields = ["id", "vehicle", "start_date", "end_date", "reason"]



class BookingSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())
    
    customer_details = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'  # Includes both customer and vehicle IDs
        extra_fields = ['customer_details', 'vehicle_details']  # Add full details separately

    def get_customer_details(self, obj):
        """Return full customer details"""
        return {
            "id": obj.customer.id,
            "first_name": obj.customer.first_name,
            "last_name": obj.customer.last_name
        } if obj.customer else None

    def get_vehicle_details(self, obj):
        """Return full vehicle details"""
        return {
            "id": obj.vehicle.id,
            "make": obj.vehicle.make,
            "model": obj.vehicle.model
        } if obj.vehicle else None



class FinalizeBookingSerializer(serializers.Serializer):
    national_id = serializers.CharField()
    street_address = serializers.CharField()
    address_line2 = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField()
    country = serializers.CharField()

    next_of_kin1_first_name = serializers.CharField()
    next_of_kin1_last_name = serializers.CharField()
    next_of_kin1_id_number = serializers.CharField()
    next_of_kin1_phone = serializers.CharField()

    pay_now = serializers.BooleanField()

    def save(self, **kwargs):
        user = self.context['request'].user
        customer = user.customer_profile
        booking_request = BookingRequest.objects.get(
            id=self.context['booking_request_id'],
            user=user,
            status='accepted'
        )

        # Update customer profile
        customer.national_id = self.validated_data['national_id']
        customer.street_address = self.validated_data['street_address']
        customer.address_line2 = self.validated_data['address_line2']
        customer.city = self.validated_data['city']
        customer.country = self.validated_data['country']

        customer.next_of_kin1_first_name = self.validated_data['next_of_kin1_first_name']
        customer.next_of_kin1_last_name = self.validated_data['next_of_kin1_last_name']
        customer.next_of_kin1_id_number = self.validated_data['next_of_kin1_id_number']
        customer.next_of_kin1_phone = self.validated_data['next_of_kin1_phone']
        customer.save()

        # Create Booking instance
        vehicle = booking_request.vehicle
        booking = Booking.objects.create(
            customer=customer,
            vehicle=vehicle,
            start_date=booking_request.start_date,
            end_date=booking_request.end_date,
            pickup_time=booking_request.pickup_time,
            dropoff_time=booking_request.dropoff_time,
            pickup_location=booking_request.pickup_location.name,
            dropoff_location=booking_request.dropoff_location.name if booking_request.dropoff_location else "",
            booking_amount=vehicle.price_per_day * ((booking_request.end_date - booking_request.start_date).days + 1),
            booking_deposit=vehicle.deposit,
            estimated_mileage=0,
            discount_amount=100 if self.validated_data['pay_now'] else 0,
            discount_description="Paid full online" if self.validated_data['pay_now'] else "Pay at counter",
            payment_method="mobile transfer" if self.validated_data['pay_now'] else "cash",
            total_amount=(vehicle.price_per_day* ((booking_request.end_date - booking_request.start_date).days + 1)) - (100 if self.validated_data['pay_now'] else 0),
            booking_request=booking_request,
            booking_status='pending'
        )

        booking_request.is_confirmed_by_customer = True
        booking_request.customer_docs_submitted = True
        booking_request.dummy_payment_done = True
        booking_request.save()
        return booking


