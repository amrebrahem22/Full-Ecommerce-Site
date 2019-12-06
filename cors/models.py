from django.db import models
from django.conf import settings

class Item(models.Model):
    title = models.CharField(max_length=155)
    price = models.FloatField()
    tiemstamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
