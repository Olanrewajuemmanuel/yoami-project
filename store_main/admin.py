from django.contrib import admin
from .models import Category, Image, Item

# Register your models here.
admin.site.register((Category, Image, Item))
