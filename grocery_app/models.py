from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

choices = (
    ('Pending', 'P'),
    ('Bought', 'B'),
    ('Not available', 'NA'),
)

# Create your models here.

class Grocery(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    # time = models.DateField(default=datetime.now(), null=True)
    status = models.CharField(max_length=20, default='Pending', choices=choices)

    class Meta:
        verbose_name = 'Groceries'
        
    def __str__(self):
        return self.name
    
class GroceryList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groceries = models.ManyToManyField(Grocery)
    time = models.DateField(null=True, default=datetime.now().date())

    class Meta:
        unique_together = ('user', 'time')

    def __str__(self):
        return str(self.user) + ' Grocery-List ' + str(self.time)

class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    groceryList = models.ManyToManyField(GroceryList)

    def __str__(self):
        return str(self.user) + ' saved-list'


