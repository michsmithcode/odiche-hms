from django.db import models
from accounts.employee_id import generate_employee_id


class EmployeeIDMixin(models.Model):
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    prefix = None   # override in child classes

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Use auto increment logic based on model count
            next_number = self.__class__.objects.count() + 1
            self.employee_id = generate_employee_id(self.prefix, next_number)

        super().save(*args, **kwargs)
