# Generated by Django 4.2.13 on 2024-06-10 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_management', '0005_rename_lattitude_store_latitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]