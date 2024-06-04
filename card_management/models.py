from django.db import models


class Card(models.Model):
    card_number = models.CharField(max_length=25, unique=True)
    driver = models.CharField(max_length=100)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.card_number
