from django.db import models
from django.contrib.auth.models import User  

class Ward(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=100, blank=True, null=True)

    def _str_(self):
        return self.name
