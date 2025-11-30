from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PermissionSerializer,HospitalRoleSerializer, TogglePermissionSerializer, RoleRequestSerializer, RolePermissionSerializer
from .permission_services import roles_permissions
from .decorators import permission_required, admin_only
from .models import Permission, HospitalRole


# Toggle permission endpoint
@extend_schema(
    summary="Enable or Disable Role Permission",
    description="Toggle a permission on/off for a role.",
    examples=[
        OpenApiExample("Enable perm", value={"role": "Pharmacist", "permission_code": "can_add_drug", "enabled": True}, request_only=True),
    ],
    tags=["permissions"],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required("can_manage_permissions")
def enable_or_disable_role_permission(request):
    serializer = TogglePermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.save()
        return Response({"detail": "success"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Get permissions for a role",
    description="Return all permissions and whether they are enabled for the supplied role.",
    request=RoleRequestSerializer,
    responses={200: RolePermissionSerializer(many=True)},
    tags=["permissions"],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required("can_manage_permissions")
def get_role_permissions(request):
    serializer_in = RoleRequestSerializer(data=request.data)
    serializer_in.is_valid(raise_exception=True)
    role = serializer_in.validated_data['role']
    try:
        qs = roles_permissions(role)
        serializer = RolePermissionSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#==================ADMIN PERMISSION CRUD==============
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@admin_only
def list_permissions(request):
    perms = Permission.objects.all()
    serializer = PermissionSerializer(perms, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@admin_only
def create_permission(request):
    serializer = PermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@admin_only
def update_permission(request, pk):
    perm = get_object_or_404(Permission, id=pk)
    serializer = PermissionSerializer(perm, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@admin_only
def delete_permission(request, pk):
    perm = get_object_or_404(Permission, id=pk)
    perm.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#========================== ROLE CRUD (Admin Only) ========================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@admin_only
def list_roles(request):
    roles = HospitalRole.objects.all()
    serializer = HospitalRoleSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@admin_only
def create_role(request):
    serializer = HospitalRoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@admin_only
def update_role(request, pk):
    role = get_object_or_404(HospitalRole, id=pk)
    serializer = HospitalRoleSerializer(role, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@admin_only
def delete_role(request, pk):
    role = get_object_or_404(HospitalRole, id=pk)
    role.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



#====================VERIFY ROLE PERMISSIONS=================================
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Permission, HospitalRole, RolePermission
from .decorators import admin_only   # if using admin restriction

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@admin_only  # optional: only admin should test
def test_permissions_system(request):
    """
    Test endpoint to verify:
    - Permissions exist
    - Roles exist
    - RolePermission mappings exist
    """
    permissions_count = Permission.objects.count()
    roles_count = HospitalRole.objects.count()
    role_permissions_count = RolePermission.objects.count()

    roles_data = []
    for role in HospitalRole.objects.all():
        perm_codes = list(
            RolePermission.objects.filter(role=role)
            .values_list("permission__code", flat=True)
        )
        roles_data.append({
            "role": role.name,
            "permissions": perm_codes,
            "permission_count": len(perm_codes)
        })

    return Response(
        {
            "status": "OK",
            "message": "Permissions system configured correctly",
            "summary": {
                "total_permissions": permissions_count,
                "total_roles": roles_count,
                "total_role_permission_mappings": role_permissions_count,
            },
            "roles_details": roles_data,
        },
        status=status.HTTP_200_OK,
    )


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from .models import Permission, HospitalRole, RolePermission
# from django.contrib.auth import get_user_model

# from .serializers import (
#     PermissionSerializer,
#     RoleSerializer,
#     RolePermissionSerializer,
#     AssignUserRoleSerializer,
#     EnableDisablePermissionSerializer,
# )

# from .role_permission import toggle_permission, get_role_permissions_list

# User = get_user_model()


# # ============================================================
# #                          PERMISSIONS CRUD
# # ============================================================

# @api_view(["POST"])
# def create_permission(request):
#     serializer = PermissionSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Permission created", "data": serializer.data}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def list_permissions(request):
#     permissions = Permission.objects.all()
#     serializer = PermissionSerializer(permissions, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["PUT"])
# def update_permission(request, pk):
#     try:
#         perm = Permission.objects.get(pk=pk)
#     except Permission.DoesNotExist:
#         return Response({"error": "Permission not found"}, status=status.HTTP_404_NOT_FOUND)

#     serializer = PermissionSerializer(perm, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Permission updated", "data": serializer.data}, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["DELETE"])
# def delete_permission(request, pk):
#     try:
#         perm = Permission.objects.get(pk=pk)
#     except Permission.DoesNotExist:
#         return Response({"error": "Permission not found"}, status=status.HTTP_404_NOT_FOUND)

#     perm.delete()
#     return Response({"message": "Permission deleted"}, status=status.HTTP_200_OK)


# # ============================================================
# #                          ROLES CRUD
# # ============================================================

# @api_view(["POST"])
# def create_role(request):
#     serializer = RoleSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Role created", "data": serializer.data}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def list_roles(request):
#     roles = HospitalRole.objects.all()
#     serializer = RoleSerializer(roles, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["PUT"])
# def update_role(request, pk):
#     try:
#         role = HospitalRole.objects.get(pk=pk)
#     except HospitalRole.DoesNotExist:
#         return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

#     serializer = RoleSerializer(role, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Role updated", "data": serializer.data}, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["DELETE"])
# def delete_role(request, pk):
#     try:
#         role = HospitalRole.objects.get(pk=pk)
#     except HospitalRole.DoesNotExist:
#         return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

#     role.delete()
#     return Response({"message": "Role deleted"}, status=status.HTTP_200_OK)


# # ============================================================
# #                  ROLE-PERMISSION MAPPING CRUD
# # ============================================================

# @api_view(["POST"])
# def enable_or_disable_permission(request):
#     """
#     Expected JSON:
#     {
#         "role_id": 1,
#         "permission_code": "can_add_patient",
#         "enabled": true
#     }
#     """
#     serializer = EnableDisablePermissionSerializer(data=request.data)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     role = serializer.validated_data["role"]
#     perm = serializer.validated_data["permission"]
#     enabled = serializer.validated_data["enabled"]

#     mapping = toggle_permission(role, perm.code, enabled)

#     return Response({
#         "message": "Permission updated for role",
#         "role": role.name,
#         "permission": perm.code,
#         "is_enabled": mapping.is_enabled
#     }, status=status.HTTP_200_OK)


# @api_view(["GET"])
# def get_role_permissions(request, role_id):
#     """
#     Get all permissions (enabled & disabled) for a role
#     """
#     try:
#         role = HospitalRole.objects.get(id=role_id)
#     except HospitalRole.DoesNotExist:
#         return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

#     data = get_role_permissions_list(role)

#     return Response({
#         "role": role.name,
#         "permissions": data
#     }, status=status.HTTP_200_OK)


# # ============================================================
# #                USER ROLE ASSIGNMENT CRUD
# # ============================================================

# @api_view(["POST"])
# def assign_role_to_user(request):
#     """
#     {
#         "user_id": 10,
#         "role_id": 3
#     }
#     """
#     serializer = AssignUserRoleSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.validated_data["user"]
#         role = serializer.validated_data["role"]

#         user.role = role
#         user.save()

#         return Response({"message": "Role assigned to user"}, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def list_users_by_role(request, role_id):
#     try:
#         role = HospitalRole.objects.get(id=role_id)
#     except HospitalRole.DoesNotExist:
#         return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

#     users = User.objects.filter(role=role)
#     data = [{"id": u.id, "email": u.email, "name": u.get_full_name()} for u in users]

#     return Response({"role": role.name, "users": data}, status=status.HTTP_200_OK)



#=================REQUIRED CRUD PERMISSIONS IN VIEWS===========
# Permissions

# Create permission

# Edit permission

# Delete permission

# List permissions

# ✔ Roles

# Create role

# Edit role

# Delete role

# List roles

# ✔ Role ↔ Permission Mapping

# Enable/disable a permission for a role

# Get a role’s permissions

# ✔ User Role Assignment

# Assign role to a user

# Change user role



#===========END POINT================
#Permissions CRUD
# create_permission

# list_permissions

# update_permission

# delete_permission
#Roles CRUD: create_role, list_roles, update_role, delete_role
#RolePermission CRUD (mapping): enable_or_disable_permission_for_role, get_role_permissions
#UserRole assignment: assign_role_to_user, list_users_by_role