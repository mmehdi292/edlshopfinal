from django.db import models

# Create your models here.
class Card(models.Model):
    cardNumber = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    mmyy = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    sold = models.FloatField(default=0)
    isblocked = models.BooleanField(default=False)


class MoneyBack(models.Model):
    cardFrom = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='cardfrom')
    cardTo = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='cardto')
    price = models.FloatField()
    dateAdded = models.DateTimeField()
    
