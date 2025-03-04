from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Vehicle, MaintenanceRecord, VehicleImage


User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')



class VehicleImageInline(admin.TabularInline):  # ✅ Allows adding multiple images per vehicle
    model = VehicleImage
    extra = 1  # Allows adding extra image slots in admin

class VehicleAdmin(admin.ModelAdmin):
    list_display = ("brand", "make", "model", "registration_number", "color", "mileage", "ownership")  # ✅ Show registration
    search_fields = ("brand", "make", "model", "registration_number")  # ✅ Enable search by registration number
    inlines = [VehicleImageInline]

admin.site.register(Vehicle, VehicleAdmin) 


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "date", "cost")