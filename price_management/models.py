from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=100)
    store_id = models.IntegerField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class StorePrice(models.Model):
    date = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    retail_price = models.FloatField()
    company_price = models.FloatField(blank=True, null=True)
    price_1 = models.FloatField(blank=True, null=True)
    price_2 = models.FloatField(blank=True, null=True)
    price_3 = models.FloatField(blank=True, null=True)
    price_4 = models.FloatField(blank=True, null=True)
    price_5 = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.date)
