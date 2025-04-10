from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Vehicle, MaintenanceRecord, VehicleImage, VehicleUnavailability, Customer, Booking


User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')


# ✅ Allows adding multiple images per vehicle
class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1  # Provides extra slots for image uploads

# ✅ Allows adding unavailability periods inside the vehicle admin panel
class VehicleUnavailabilityInline(admin.TabularInline):
    model = VehicleUnavailability
    extra = 1  # Allows quick addition of unavailability periods

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("make", "model", "registration_number", "color", "mileage", "price_per_day", "ownership")
    list_filter = ("ownership", "make", "model")
    search_fields = ("make", "model", "registration_number")
    inlines = [VehicleImageInline, VehicleUnavailabilityInline]  # ✅ Includes Images & Unavailability


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "date", "cost")


@admin.register(VehicleUnavailability)
class VehicleUnavailabilityAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "start_date", "end_date", "reason")
    list_filter = ("start_date", "end_date", "reason")
    search_fields = ("vehicle__make", "vehicle__model", "reason")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number","email","last_booking_date")
    search_fields = ("first_name", "last_name", "phone_number", "email", "national_id")
    list_filer = ("last_booking_date", "phone_number", "email", "national_id")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer", "vehicle", "start_date", "end_date", "booking_status")
    list_filter = ("booking_status", "start_date", "end_date")
    search_fields = ("customer__first_name", "customer__last_name", "vehicle__make", "vehicle__model")

