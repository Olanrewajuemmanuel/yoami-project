from django.contrib import admin
from .models import Category, Item, Image

# Register your models here.
admin.site.register((Category, Item, Image))