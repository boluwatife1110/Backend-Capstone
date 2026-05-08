from rest_framework.permissions import BasePermission

class IsSellerOrAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type in ['seller', 'agent']