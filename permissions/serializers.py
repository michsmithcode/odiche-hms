from rest_framework import serializers
from .models import Permission, HospitalRole, RolePermission, UserProfile
from django.shortcuts import get_object_or_404


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "description"]

class HospitalRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalRole
        fields = ["id", "name", "description"]

class RolePermissionSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(read_only=True)
    permission_id = serializers.UUIDField(write_only=True, required=True)
    role_id = serializers.UUIDField(write_only=True, required=True)

    class Meta:
        model = RolePermission
        fields = ["id", "role_id", "permission_id", "permission", "is_enabled"]

    def create(self, validated_data):
        role = get_object_or_404(HospitalRole, id=validated_data['role_id'])
        perm = get_object_or_404(Permission, id=validated_data['permission_id'])
        obj, _ = RolePermission.objects.update_or_create(
            role=role, permission=perm, defaults={'is_enabled': validated_data.get('is_enabled', True)}
        )
        return obj
    
     
    def update(self, instance, validated_data):
        instance.is_enabled = validated_data.get("is_enabled", instance.is_enabled)
        instance.save()
        return instance




class UserProfileSerializer(serializers.ModelSerializer):
    role = HospitalRoleSerializer(read_only=True)
    role_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'role_id']

    def update(self, instance, validated_data):
        role_id = validated_data.get('role_id')
        if role_id:
            role = get_object_or_404(HospitalRole, id=role_id)
            instance.role = role
            instance.save()
        return instance



class TogglePermissionSerializer(serializers.Serializer):
    role = serializers.CharField()
    permission_code = serializers.CharField()
    enabled = serializers.BooleanField()

    def validate(self, data):
        #from .models import HospitalRole, Permission
        role = HospitalRole.objects.filter(name=data['role']).first()
        if not role:
            raise serializers.ValidationError("Invalid role")
        perm = Permission.objects.filter(code=data['permission_code']).first()
        if not perm:
            raise serializers.ValidationError("Invalid permission_code")
        data['role_obj'] = role
        data['perm_obj'] = perm
        return data

    def save(self):
        from .permission_services import toggle_permission
        role_obj = self.validated_data['role_obj']
        perm_obj = self.validated_data['perm_obj']
        enabled = self.validated_data['enabled']
        mapping = toggle_permission(role_obj=role_obj, perm_obj=perm_obj, enabled=enabled) #role_name=role_obj.name, code=code,
        return mapping



#================ ASSIGNING USER TO THEIR RESPECTIVE ROLES ======================
class AssignUserRoleSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    role_id = serializers.UUIDField(write_only=True, required=True)


    def validate(self, data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        #from .models import HospitalRole, UserProfile

        user = User.objects.filter(id=data['user_id']).first()
        if not user:
            raise serializers.ValidationError("Invalid user_id")

        role = HospitalRole.objects.filter(id=data['role_id']).first()
        if not role:
            raise serializers.ValidationError("Invalid role_id")

        data['user'] = user
        data['role'] = role
        return data

    def save(self):
        #from .models import UserProfile
        user = self.validated_data['user']
        role = self.validated_data['role']
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()
        return profile

#===================Role Request======================

class RoleRequestSerializer(serializers.Serializer):
    role = serializers.CharField()




