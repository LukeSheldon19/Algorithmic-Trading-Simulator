# Generated by Django 4.2.11 on 2024-04-17 20:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('sector', models.CharField(max_length=100)),
                ('num_employee', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('industry', models.CharField(max_length=100)),
                ('end_fiscal_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Composed_of',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('ticker', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('share_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('portfolio_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('composition', models.ManyToManyField(through='myApp.Composed_of', to='myApp.share')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('close_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('volume', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.share')),
            ],
        ),
        migrations.AddField(
            model_name='composed_of',
            name='portfolio_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.portfolio'),
        ),
        migrations.AddField(
            model_name='composed_of',
            name='ticker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.share'),
        ),
    ]
