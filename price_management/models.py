from django.db import models


class StorePrice(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    store_id = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    retail_price = models.FloatField()
    price_1 = models.FloatField(null=True, blank=True)
    price_2 = models.FloatField(null=True, blank=True)
    price_3 = models.FloatField(null=True, blank=True)
    price_4 = models.FloatField(null=True, blank=True)
    price_5 = models.FloatField(null=True, blank=True)
