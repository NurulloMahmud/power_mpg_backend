# Generated by Django 4.2.13 on 2024-06-04 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StorePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('store_id', models.IntegerField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=10)),
                ('retail_price', models.FloatField()),
                ('price_1', models.FloatField(blank=True, null=True)),
                ('price_2', models.FloatField(blank=True, null=True)),
                ('price_3', models.FloatField(blank=True, null=True)),
                ('price_4', models.FloatField(blank=True, null=True)),
                ('price_5', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]