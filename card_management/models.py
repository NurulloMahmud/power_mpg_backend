from django.db import models
from datetime import datetime


class Card(models.Model):
    card_number = models.CharField(max_length=25, unique=True)
    driver = models.CharField(max_length=100)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_number

    def save(self, *args, **kwargs):
        if not self.pk:
            CardDriverHistory.objects.create(card=self, driver=self.driver, beg_date=self.created_at)
        else:
            card_driver = CardDriverHistory.objects.get(card=self, driver=self.driver, end_date__isnull=True)
            if self.driver != card_driver.driver:
                card_driver.end_date = datetime.now()
                card_driver.save()
                CardDriverHistory.objects.create(card=self, driver=self.driver, beg_date=self.created_at)
        super().save(*args, **kwargs)

class CardDriverHistory(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    driver = models.CharField(max_length=100)
    beg_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.driver
