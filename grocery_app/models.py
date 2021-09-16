from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Grocery(models.Model):
    name = models.CharField(max_length=40)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    time = models.DateTimeField(default=datetime.now())

    class Meta:
        verbose_name = 'grocerie'

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groceries = models.ManyToManyField(Grocery)


