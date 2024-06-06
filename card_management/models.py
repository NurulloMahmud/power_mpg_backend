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

class FuelTransactions(models.Model):
    from price_management.models import StorePrice
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()
    gallons = models.FloatField()
    retail_price = models.FloatField()
    discounted_price = models.FloatField()
    amount_saved = models.FloatField()
    store = models.ForeignKey(StorePrice, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        from price_management.models import StorePrice
        if not self.pk:
            store_price = StorePrice.objects.filter(date=self.date).first()
        super().save(*args, **kwargs)