from django.utils import timezone
from django.shortcuts import render
from django.views import generic
from django.http import Http404

from .models import Item
from cart.models import Cart, CartItem
from .globals import CATEGORIES
from .forms import SearchItemForm

# Create your views here.

def index_view(request):
    template_name = 'store_main/index.html'

    context = {
        'items': Item.objects.filter(date_added__lte=timezone.now()).order_by("-date_added"),
        'form': SearchItemForm(),
        'cart_qty': CartItem.objects.filter(cart__user=request.user).count() if request.user.is_authenticated else 0
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
            min_price = form.cleaned_data['price_min'] or 0 # optional, if field was left blank
            max_price = form.cleaned_data['price_max'] or 1000
            found_items = Item.objects.filter(title__icontains=item_name, category__category_name__in=item_category, price__range=(
                min_price, max_price)).order_by("-date_added").distinct()
            if not found_items:
                context['error_msg'] = ("No product to view.")
            context['found_items'] = found_items

        else:
            context['error_msg'] = form.errors

    context['form'] = form
    context['cart_qty'] = Cart.objects.filter(user=request.user) if request.user.is_authenticated else 0


    return render(request, template_name, context)

class ItemDetailView(generic.DetailView):
    template_name = 'store_main/item_details.html'
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchItemForm()
        context['cart_qty'] = Cart.objects.filter(user=self.request.user).count() if self.request.user.is_authenticated else 0


        return context



