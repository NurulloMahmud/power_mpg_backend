# Generated by Django 4.2.13 on 2024-07-01 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('card_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.company'),
        ),
    ]
