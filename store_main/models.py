import datetime
from tabnanny import verbose

from django.db import models
from django.utils import timezone

# Create your models here.

# TODO: Add category -> many items *-* many categories

class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    HEADWEAR = 'HW'
    APPARELS = 'APPA'
    TOYS = 'TOYS'
    PROPS = 'PROPS'
    OTHERS = 'OTH'
    CATEGORIES = [
        (HEADWEAR, 'HEADWEAR'),
        (APPARELS, 'APPARELS'),
        (TOYS,  'TOYS'),
        (PROPS,  'PROPS'),
        (OTHERS, 'OTHERS'),
    ]

    category_name = models.CharField(max_length=5, choices=CATEGORIES, default=OTHERS)

class Item(models.Model):
    category = models.ManyToManyField(Category)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percentage = models.IntegerField(default=0)
    desc = models.TextField(max_length=1024)
    title = models.CharField(max_length=255)
    stock_available = models.IntegerField(default=0)
    date_added = models.DateTimeField('date_added')

    def __str__(self):
        return self.title

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_added <= now



class Image(models.Model):
    item_name = models.ForeignKey(Item, on_delete=models.PROTECT)
    path_to_img = models.FileField(upload_to='uploads/')
    date_created = models.DateTimeField()

