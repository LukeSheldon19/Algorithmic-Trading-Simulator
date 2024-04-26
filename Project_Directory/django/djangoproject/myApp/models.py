
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Company(models.Model):
    name = models.CharField(unique=True,max_length=100)
    sector = models.CharField(max_length=100)
    num_employee = models.IntegerField(validators=[MinValueValidator(0)])
    industry = models.CharField(max_length=100)
    end_fiscal_year = models.DateField()
    
    def __str__(self):
        return self.name

class Share(models.Model):
    ticker = models.CharField(primary_key=True,max_length=5)
    type = models.CharField(max_length=100)
    #share_price = models.DecimalField(max_digits=10, decimal_places=2)     //Getting rid of share_price, this attribute can just be grabbed from Data attribute
    #available = models.IntegerField(validators=[MinValueValidator(0)])     //Getting rid of available, can just be grabbed from Data table
    id = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticker


class Data(models.Model):
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField(validators=[MinValueValidator(0)])
    ticker = models.ForeignKey(Share, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ticker) + ' Data'
    
class Portfolio(models.Model):
    portfolio_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    composition = models.ManyToManyField(Share, through='Composed_of')

    def __str__(self):
        return self.name

class Composed_of(models.Model):
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Share, on_delete=models.CASCADE)
    num_shares = models.IntegerField(validators=[MinValueValidator(0)],default=0)

    def __str__(self):
        return str(self.portfolio_id) + ' Composition'



    
