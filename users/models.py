from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    price_category = models.PositiveIntegerField(null=True, blank=True) # remove null later
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    mailing_address = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk and not self.is_superuser:
            self.is_active = False
        super().save(*args, **kwargs)
