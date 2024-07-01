# Generated by Django 4.2.13 on 2024-07-01 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=25, unique=True)),
                ('driver', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.BooleanField(default=False)),
                ('last_digits', models.CharField(blank=True, max_length=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CardDriverHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.CharField(blank=True, max_length=25, null=True)),
                ('driver', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('beg_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
