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

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.company:
                company, created = "users.Company.objects.get_or_create(name='PowerMPG', owner='PowerMPG', phone_number='', email='', price_category=1, is_active=True)"
            else:
                company = self.company
            CardDriverHistory.objects.create(card=self, driver=self.driver, beg_date=self.created_at, company=company)
        else:
            card_driver = CardDriverHistory.objects.get(card=self, end_date__isnull=True)
            if self.driver != card_driver.driver:
                card_driver.end_date = datetime.now()
                card_driver.save()
                CardDriverHistory.objects.create(card=self, driver=self.driver, beg_date=datetime.now(), company=self.company)
        super().save(*args, **kwargs)

class CardDriverHistory(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    driver = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, null=True, blank=True)
    beg_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.driver
