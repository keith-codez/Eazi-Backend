from rest_framework import serializers
from .models import User, Customer, Agency, Agent
from django.contrib.auth import authenticate

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.role = 'CUSTOMER'
        user.save()

        # Create Agent profile with the given first_name, last_name, and user reference
        Agent.objects.create(user=user, first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        
        return user


class AgentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.role = 'AGENT'
        user.save()

        # Create Agent profile with the given first_name, last_name, and user reference
        Agent.objects.create(user=user, first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        
        return user


class AgencyRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'name')

    def create(self, validated_data):
        agency_name = validated_data.pop('name')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='agency'
        )
        Agency.objects.create(name=agency_name, created_by=user)
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



class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = "__all__"


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"