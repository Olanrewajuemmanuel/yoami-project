from django.utils import timezone
from django.shortcuts import render

from .models import Item
from .globals import CATEGORIES
from .forms import SearchItemForm

# Create your views here.


def index_view(request):
    template_name = 'store_main/index.html'

    context = {
        'items': Item.objects.filter(date_added__lte=timezone.now()).order_by("-date_added"),
        'form': SearchItemForm(),
    }

    return render(request, template_name, context)


def search_detail(request):
    template_name = 'store_main/search_details.html'
    context = {}

    if request.GET:
        form = SearchItemForm(request.GET)

        if form.is_valid():
            item_name = form.cleaned_data['item_name']
            item_category = form.cleaned_data['category']
            min_price = form.cleaned_data['price_min'] or 0
            max_price = form.cleaned_data['price_max'] or 1000
        try:
            found_items = Item.objects.filter(title__icontains=item_name, category__category_name__in=item_category, price__range=(
                min_price, max_price)).order_by("-date_added").distinct()
            context['found_items'] = found_items
            print(found_items)
        except (KeyError, Item.DoesNotExist):
            context['error_msg'] = "There was an error fetching the item. Please try again later."
        else:
            context['error_msg'] = form.errors

    context['form'] = form

    return render(request, template_name, context)
