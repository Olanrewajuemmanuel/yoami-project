from urllib import response
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

import json

from .models import CartItem
from store_main.models import Item

# Create your views here.

class CartListView(generic.ListView):
    template_name = 'cart/cart.html'
    model = CartItem
    context_object_name = 'cart_items_list'

    def get_queryset(self):
        # Get user's cart list
        print(self.kwargs)
        return CartItem.objects.filter(user=self.request.user)

def update_cart_view(request):
    user = request.user
    response = json.loads(request.body)
    item_id = response.get('itemId')
    action = response.get('reqType')
    # if cartitem does not exist, create a new object
    item = Item.objects.get(pk=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=user, saved_item=item)
    
    if action == 'add':
        cart_item.item_qty += 1
        cart_item.save()
    elif action == 'remove':
        cart_item.item_qty -= 1
        cart_item.save()
    
    if cart_item.item_qty == 0:
        cart_item.delete()

    return JsonResponse({'quantity': cart_item.item_qty, 'code': 'ok'})
