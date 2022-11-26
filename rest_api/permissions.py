from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission


class APIPermissionBaseView(BasePermission):
    message = 'You do not have permissions to access this API'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    endpoint_permission = None

    def get_endpoint_permission(self):
        if not self.endpoint_permission:
            raise ValueError('endpoint_permission is empty, Please provide a permission')
        return self.endpoint_permission

    def has_permission(self, request, view):
        user_permissions = request.user.get_all_permissions()
        if self.get_endpoint_permission() in user_permissions:
            return True
        return False