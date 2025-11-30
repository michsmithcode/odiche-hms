# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import PharmacyCashier


# @receiver(post_save, sender=PharmacyCashier)
# def generate_employee_id(sender, instance, created, **kwargs):
#     if created and not instance.employee_id:
#         short_uuid = str(instance.user.id)[:8]
#         instance.employee_id = f"CASH-{short_uuid}"
#         instance.save()
