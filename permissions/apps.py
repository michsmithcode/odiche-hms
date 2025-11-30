from django.apps import AppConfig
from django.db.models.signals import post_migrate

class PermissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'permissions'

    def ready(self):
        from . import signals   # connect post_migrate signal in signals.py
 

 



# from django.apps import AppConfig
# from django.db.models.signals import post_migrate
# from django.conf import settings 

# def create_default_permissions(sender, **kwargs):
#     """This runs after migrations of this app have been applied."""
#     from .models import Permission # imported inside to avoid AppRegistryNotReady
#     #    Loop through all the defined permissions
#     for code, group, desc in settings.ALL_PHARMACY_EMPLOYEES_PERMISSIONS:
#         Permission.objects.get_or_create(code=code, defaults={'group':group,'description': desc})


# class PermissionsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'permissions'
    
#     def ready(self):
#         # Connect our function to Django's post_migrate signal.
#         post_migrate.connect(create_default_permissions,sender=self)
