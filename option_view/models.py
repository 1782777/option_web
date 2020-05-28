from django.db import models

# Create your models here.
class options(models.Model):
    class Meta:
        db_table='options'
    code = models.CharField(max_length=20,default='')
    name = models.CharField(max_length=20,default='')
    price = models.FloatField()
    eprice = models.FloatField()
    eday = models.DateField()
    day = models.DateField()
    iv = models.FloatField()
    # name_op = models.CharField(max_length=20,default='')

class iv_mean(models.Model):
    class Meta:
        db_table='iv_mean'
    time = models.TimeField()
    iv = models.FloatField()
    target = models.CharField(max_length=20)

class volume(models.Model):
    class Meta:
        db_table='volume'
    volume = models.FloatField()

class etf(models.Model):
    class Meta:
        db_table='etf'
    time = models.TimeField()
    etf_50 = models.FloatField(null=True)
    etf_300 = models.FloatField(null=True)
    es = models.FloatField(null=True)
    etf_hs = models.FloatField(null=True)
    etf_sz = models.FloatField(null=True)




