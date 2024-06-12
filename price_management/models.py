from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=100)
    store_id = models.CharField(max_length=20)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and self.name.lower() == "pilot":
            self.name = "Pilot / Flying J"
        super(Store, self).save(*args, **kwargs)

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
