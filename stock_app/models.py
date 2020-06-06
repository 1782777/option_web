from django.db import models

# Create your models here.
class stock_vol(models.Model):
    class Meta:
        db_table='stock_vol'
    code = models.CharField(max_length=20,default='')
    name = models.CharField(max_length=20,default='')
    vol = models.FloatField()
    vol_day_mean = models.FloatField()
    change = models.DateField()
    date = models.DateField()
    
