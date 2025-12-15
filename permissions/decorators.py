from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .permission_services import user_has_permission

def permission_required(permission_code: str):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
            if not user_has_permission(request.user, permission_code):
                return Response({'detail': f'Permission denied: {permission_code}'}, status=status.HTTP_403_FORBIDDEN)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def any_permission_required(*permissions):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
            for perm in permissions:
                if user_has_permission(request.user, perm):
                    return view_func(request, *args, **kwargs)
            return Response({'detail': f'Permission denied. Required any of: {permissions}'}, status=status.HTTP_403_FORBIDDEN)
        return wrapper
    return decorator


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Get role from user
            try:
                user_role = getattr(request.user, 'role') or getattr(request.user.profile, 'role')
            except:
                user_role = None

            # Converting role instance to string 
            if hasattr(user_role, "name"):
                user_role = user_role.name

            if user_role not in roles:
                return Response({'detail': f'Role {user_role} not allowed. Required: {roles}'}, status=status.HTTP_403_FORBIDDEN)

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


# def role_required(*roles):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
#             user_role = None
            
            
#             try:
#                 user_role = getattr(request.user, 'profile').role.name if getattr(request.user, 'profile', None) else getattr(request.user, 'role', None)
#             except Exception:
#                 user_role = getattr(request.user, 'role', None)
#             if isinstance(user_role, str):
#                 if user_role not in roles:
#                     return Response({'detail': f'Role {user_role} not allowed. Required: {roles}'}, status=status.HTTP_403_FORBIDDEN)
#             else:
#                 if user_role is None or user_role.name not in roles:
#                     return Response({'detail': f'Role not allowed. Required: {roles}'}, status=status.HTTP_403_FORBIDDEN)
#             return view_func(request, *args, **kwargs)
#         return wrapper
#     return decorator


#Admin only permission decorator 
def admin_only(view_func):
    """Restrict certain endpoints to Hospital_Admin & Main_Admin."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=401)
        
        # Fetch role properly
        role = None
        try:
            if hasattr(request.user, "profile") and request.user.profile.role:
                role = request.user.profile.role.name
            elif hasattr(request.user, "role"):  # fallback if user model has role directly
                role = request.user.role
        except:
            role = None

        if role not in ["Main_Admin", "Hospital_Admin"]:
            return Response({"detail": "Admin access only"}, status=403)

        return view_func(request, *args, **kwargs)
    return _wrapped