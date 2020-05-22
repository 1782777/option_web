from django.db import models

# Create your models here.
class option(models.Model):
    code = models.CharField(max_length=20)
    price = models.FloatField()
    eprice = models.FloatField()
    time = models.DateTimeField()
    iv = models.FloatField()
    name_op = models.CharField(max_length=20,default='')

class iv_mean(models.Model):
    time = models.DateTimeField()
    iv = models.FloatField()
    target = models.CharField(max_length=20)



