from  rest_framework.permissions import BasePermission

class isowner(BasePermission):
    message='You are not the owner of these post'
    my_safe_method=['PUT']
    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False
    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_method:
            return True
        return obj.user==request.user