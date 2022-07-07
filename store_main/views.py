from django.utils import timezone
from django.shortcuts import render
from django.views import generic

from .models import Item

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'store_main/index.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')[:30]
