# Generated by Django 4.2.13 on 2024-06-07 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeprice',
            name='company_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
