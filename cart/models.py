from django.db import models
from django.contrib.auth.models import User

from store_main.models import Item

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_item = models.OneToOneField(Item, on_delete=models.SET_NULL, null=True)
    item_qty = models.IntegerField(default=0)

    def __str__(self):
        return self.saved_item.title

