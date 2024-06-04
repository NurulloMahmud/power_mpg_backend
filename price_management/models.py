from django.db import models


class StorePrice(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    location_id = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    retail_price = models.FloatField()
    price_1 = models.FloatField()
    price_2 = models.FloatField()
    price_3 = models.FloatField()
