# Generated by Django 4.2.11 on 2024-04-25 17:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_alter_share_ticker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='composed_of',
            name='percent',
        ),
        migrations.AddField(
            model_name='composed_of',
            name='num_shares',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
