from django.db import models
from django.contrib.auth.models import User

from store_main.models import Item

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_qty = models.CharField(default=0, max_length=100)

    def __str__(self):
        return self.saved_item.title

