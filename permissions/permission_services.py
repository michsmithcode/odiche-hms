from django.shortcuts import get_object_or_404
from .models import Permission, RolePermission, HospitalRole
from django.db import transaction


def toggle_permission(hospital_role, role_name: str, code: str, enabled: bool):
    """
    Toggle a single permission for a role (single-hospital system).
    `hospital_role` expected to be a HospitalRole instance OR None.
    If you pass role_name it will find/create the role entry in HospitalRole (idempotent).
    """
    perm = get_object_or_404(Permission, code=code)

    role_obj = None
    if isinstance(hospital_role, HospitalRole):
        role_obj = hospital_role
    else:
        role_obj = get_object_or_404(HospitalRole, name=role_name)

    mapping, created = RolePermission.objects.get_or_create(
        role=role_obj,
        permission=perm,
        defaults={'is_enabled': enabled}
    )
    if not created:
        if mapping.is_enabled != enabled:
            mapping.is_enabled = enabled
            mapping.save()
    return mapping

def roles_permissions(role_name):
    """
    Return queryset of RolePermission for the named role.
    """
    role = get_object_or_404(HospitalRole, name=role_name)
    return RolePermission.objects.filter(role=role).select_related("permission")

def user_has_permission(user, perm_code: str) -> bool:
    """
    Check whether the authenticated user has the given permission.
    Supports:
      - request.user.profile.role (UserProfile.role)
      - request.user.role attribute (string or FK)
    Main_Admin gets all permissions.
    """
    if not user or not user.is_authenticated:
        return False

    # Get role from profile first
    role = None
    try:
        profile = getattr(user, "profile", None)
        if profile:
            role = profile.role
    except Exception:
        role = None

    # Fallback if user has role attribute (string or FK)
    if role is None:
        user_role_attr = getattr(user, "role", None)
        if isinstance(user_role_attr, HospitalRole):
            role = user_role_attr
        elif isinstance(user_role_attr, str):
            role = HospitalRole.objects.filter(name__iexact=user_role_attr).first()

    if role is None:
        return False

    if role.name.lower() in ("main_admin", "main-admin", "main admin"):
        return True

    return RolePermission.objects.filter(role=role, permission__code=perm_code, is_enabled=True).exists()



