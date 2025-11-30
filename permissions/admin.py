from django.contrib import admin
from .models import Permission, HospitalRole, RolePermission, UserProfile

admin.site.register(Permission)
admin.site.register(HospitalRole)
admin.site.register(RolePermission)
admin.site.register(UserProfile)

