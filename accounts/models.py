from django.db import models


class AccountType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Account(models.Model):
    from users.models import Company
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.company.name