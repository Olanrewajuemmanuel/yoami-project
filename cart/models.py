from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from store_main.models import Item

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    saved_item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    item_qty = models.IntegerField(default=0)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.saved_item.title
