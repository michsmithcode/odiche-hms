from rest_framework.permissions import BasePermission

class IsCashierOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_staff:
            return True
        
        # Cashier can access only their own profile
        return obj.user == request.user
