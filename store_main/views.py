from django.utils import timezone
from django.shortcuts import render
from django.views import generic

from .models import Item, Category

# Create your views here.

def index_view(request):
    template_name = 'store_main/index.html'

    context = {
        'items': Item.objects.filter(date_added__lte=timezone.now()).order_by("-date_added"),
    }
    
    return render(request, template_name, context)

def search_detail(request):
    template_name = 'store_main/search.html'
    context = {}
    

    try:
        item_name = request.GET['search']
        item_category = request.GET['categories']
        min_price_filter = request.GET['min']
        max_price_filter = request.GET['max']

        found_item = Item.objects.filter(title__icontains=item_name, category__category_name=item_category)
        print(found_item)
        context['found_item'] = found_item
    except (KeyError, Item.DoesNotExist):
        context['error_msg'] = "There was an error when searching the item, try again."

    return render(request, template_name, context)
