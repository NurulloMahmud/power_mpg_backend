from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.username
