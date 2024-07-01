# Generated by Django 4.2.13 on 2024-07-01 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('store_id', models.CharField(max_length=20)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=10)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StorePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('retail_price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('company_price', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('price_1', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('price_2', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('price_3', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('price_4', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('price_5', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='price_management.store')),
            ],
        ),
    ]
