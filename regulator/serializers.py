from rest_framework import serializers
from .models import User, Customer
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    # Allow missing fields by setting required=False
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    email = serializers.EmailField(required=False, allow_null=True)
    national_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    drivers_license = serializers.ImageField(required=False, allow_null=True)

    # Next of kin fields should be optional
    next_of_kin1_first_name = serializers.CharField(required=False, allow_blank=True)
    next_of_kin1_last_name = serializers.CharField(required=False, allow_blank=True)
    next_of_kin1_id_number = serializers.CharField(required=False, allow_blank=True)
    next_of_kin1_phone = serializers.CharField(required=False, allow_blank=True)

    next_of_kin2_first_name = serializers.CharField(required=False, allow_blank=True)
    next_of_kin2_last_name = serializers.CharField(required=False, allow_blank=True)
    next_of_kin2_id_number = serializers.CharField(required=False, allow_blank=True)
    next_of_kin2_phone = serializers.CharField(required=False, allow_blank=True)

    last_booking_date = serializers.DateField(required=False, allow_null=True)
