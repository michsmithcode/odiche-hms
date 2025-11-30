# permissions/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from .constant import PERMISSIONS, ROLES, ROLE_PERMISSION_MAP

@receiver(post_migrate, weak=False)
def create_default_permissions(sender, **kwargs):
    # run only for this app
    if sender.name != 'permissions':
        return

    Permission = apps.get_model('permissions', 'Permission')
    HospitalRole = apps.get_model('permissions', 'HospitalRole')
    RolePermission = apps.get_model('permissions', 'RolePermission')

    # Create permissions
    created_perms = {}
    for code, desc in PERMISSIONS:
        p, _ = Permission.objects.get_or_create(code=code, defaults={'description': desc})
        created_perms[code] = p

    # Create roles
    created_roles = {}
    for r in ROLES:
        role_obj, _ = HospitalRole.objects.get_or_create(name=r, defaults={'description': f'{r} role'})
        created_roles[r] = role_obj

    # Grant mapped permissions
    for role_name, perm_list in ROLE_PERMISSION_MAP.items():
        role_obj = created_roles.get(role_name)
        if not role_obj:
            continue
        if "ALL" in perm_list:
            # attach all permissions
            for perm in created_perms.values():
                RolePermission.objects.update_or_create(role=role_obj, permission=perm, defaults={'is_enabled': True})
        else:
            for code in perm_list:
                perm = created_perms.get(code)
                if perm:
                    RolePermission.objects.update_or_create(role=role_obj, permission=perm, defaults={'is_enabled': True})





# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from django.contrib.auth.models import Group, Permission
# from permissions.constant import ROLE_PERMISSIONS


# @receiver(post_migrate)
# def create_role_groups(sender, **kwargs):
#     """
#     Create role-based groups and assign permissions after migration.
#     """
#     if sender.name == "permissions":  # only run when this app migrates
#         for role, perms in ROLE_PERMISSIONS.items():
#             group, _ = Group.objects.get_or_create(name=role.capitalize())

#             # Get permissions and assign
#             group_permissions = Permission.objects.filter(codename__in=perms)
#             group.permissions.set(group_permissions)
#             group.save()
