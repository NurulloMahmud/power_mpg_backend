from django.db import models
from datetime import datetime



class Card(models.Model):
    card_number = models.CharField(max_length=25, unique=True)
    driver = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_number

class CardDriverHistory(models.Model):
    card = models.CharField(max_length=25, null=True, blank=True)
    driver = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    beg_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.driver
