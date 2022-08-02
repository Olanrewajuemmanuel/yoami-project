from django.db import models
from django.utils import timezone

# Create your models here.

class OrderDetailItem(models.Model):
    user_id = models.CharField(max_length=255)
    order_email = models.EmailField(null=True)
    product_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.order_email

