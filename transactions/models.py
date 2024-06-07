from django.db import models



class Transaction(models.Model):
    from card_management.models import Card
    from price_management.models import Store

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    driver = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    retail_price = models.FloatField()
    client_price = models.FloatField() # show client
    company_price = models.FloatField() # show our company only | only admin sees it
    quantity = models.FloatField()
    retail_amount = models.FloatField()
    client_amount = models.FloatField()
    company_amount = models.FloatField()
    item = models.CharField(max_length=100)
    client_profit = models.FloatField()
    company_profit = models.FloatField()
    transaction_fee = models.FloatField(default=0)
    location_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.card
    
    def save(self, *args, **kwargs):
        from price_management.models import StorePrice
        if not self.pk:
            price_category = int(self.card.company.price_category)
            self.company = self.card.company.name

            if self.item == 'ULSD':
                self.transaction_fee = 1.5
                self.item = "Fuel"
                store_price = StorePrice.objects.filter(sotre=self.store, date=self.date).first()
                self.company_price = store_price.company_price

                # get fuel price for client
                if price_category == 1:
                    client_price = store_price.price_1
                elif price_category == 2:
                    client_price = store_price.price_2
                elif price_category == 3:
                    client_price = store_price.price_3
                elif price_category == 4:
                    client_price = store_price.price_4
                else:
                    client_price = store_price.price_5
            elif self.item == 'DEFD':
                self.item = "DEF"
                client_price = self.retail_price
                self.company_price = self.retail_price
            elif self.item in ["SCLE", "STAX"]:
                self.item = "Scale"
                client_price = self.retail_price
                self.company_price = self.retail_price
            else: 
                client_price = self.retail_price
                self.company_price = self.retail_price
            
            self.client_price = float(client_price)
            self.company_price = store_price.company_price
            self.retail_amount = self.retail_price * self.quantity
            self.client_amount = self.client_price * self.quantity
            self.company_amount = self.company_price * self.quantity
            self.client_profit = self.retail_amount - self.client_amount - self.transaction_fee
            self.company_profit = (self.retail_amount - self.company_amount - self.client_profit) + self.transaction_fee

        super().save(*args, **kwargs)