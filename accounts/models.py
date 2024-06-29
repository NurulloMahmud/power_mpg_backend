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

class Payment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.account.company.name
    
    def save(self, *args, **kwargs):
        from transactions.models import Transaction

        if not self.pk:
            payment_amount = self.amount
            transactions = Transaction.objects.filter(company=self.account.company, debt__gt=0)

            for transaction in transactions:
                if payment_amount > transaction.debt:
                    payment_amount -= transaction.debt
                    transaction.debt = 0
                    transaction.save()
                else:
                    transaction.debt -= payment_amount
                    payment_amount = 0
                    transaction.save()
                    break

            if payment_amount > 0:
                self.account.balance += payment_amount
                self.account.save()

        super(Payment, self).save(*args, **kwargs)
