from django.db import models
from decimal import Decimal



class TransactionManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().order_by('date', 'time')

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
    unit_number = models.CharField(max_length=100, null=True, blank=True)
    retail_price = models.DecimalField(max_digits=10, decimal_places=3)
    client_price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # show client
    company_price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # show our company only | only admin sees it
    quantity = models.FloatField()
    retail_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    client_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    company_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    item = models.CharField(max_length=100)
    client_profit = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    company_profit = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    transaction_fee = models.FloatField(default=0)
    location_name = models.CharField(max_length=100, null=True, blank=True)
    debt = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    objects = TransactionManager()

    def __str__(self):
        return self.card
    
    class Meta:
        ordering = ['date', 'time']
    
    def save(self, *args, **kwargs):
        from price_management.models import StorePrice
        from accounts.models import Account

        if not self.pk:
            price_category = int(self.card.company.price_category)
            self.company = self.card.company.name
            store_price = StorePrice.objects.filter(store=self.store, date=self.date).first()

            if self.item == 'ULSD':
                self.transaction_fee = 1.5
                self.item = "Fuel"
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
            
            self.client_price = Decimal(client_price)
            self.retail_amount = Decimal(self.retail_price) * Decimal(self.quantity)
            self.client_amount = self.client_price * Decimal(self.quantity)
            self.company_amount = Decimal(self.company_price) * Decimal(self.quantity)
            self.client_profit = self.retail_amount - self.client_amount - Decimal(self.transaction_fee)
            self.company_profit = (self.retail_amount - self.company_amount - self.client_profit) + Decimal(self.transaction_fee)
            self.debt = Decimal(self.client_amount)

            account = Account.objects.get(company=self.card.company)
            account.balance -= self.client_amount
            account.save()

        super().save(*args, **kwargs)

