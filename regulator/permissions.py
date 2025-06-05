from rest_framework.permissions import BasePermission

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'agent'


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'


class IsOwnerOfBookingRequest(BasePermission):
    """
    Ensure that only the owner of the booking request can access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user