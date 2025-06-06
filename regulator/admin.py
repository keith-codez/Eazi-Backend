from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Agent, Agency
from staff.models import Location


User = get_user_model()

admin.site.register(Agent)



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "role")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "role", "password1", "password2"),
        }),
    )

    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


class AgentInline(admin.StackedInline):  # or TabularInline if preferred
    model = Agent
    extra = 1
    fields = ['user']  # add more fields if needed
    

class LocationInline(admin.StackedInline):
    model = Location
    extra = 1
    fields = ['name', 'address', 'city', 'coordinates']

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    inlines = [LocationInline,AgentInline]
    list_display = ('name', 'number_of_employees')


