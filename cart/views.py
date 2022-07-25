from re import template
from urllib import response
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views import generic

import json

from .models import Cart, CartItem
from store_main.models import Item

# Create your views here.

class CartListView(generic.ListView):
    template_name = 'cart/cart.html'
    model = Cart
    context_object_name = 'user_cart'

    def get_queryset(self):
        # Get user's cart list
        return Cart.objects.get(user=self.request.user) if self.request.user.is_authenticated else 0

def update_cart_view(request):
    user = request.user
    response = json.loads(request.body)
    item_id = response.get('itemId')
    action = response.get('reqType')
    # if cartitem does not exist, create a new object
    item = Item.objects.get(pk=item_id)
    user_cart = Cart.objects.get(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, saved_item=item)
    
    if action == 'add':
        cart_item.item_qty += 1
        cart_item.save()
    elif action == 'remove':
        cart_item.item_qty -= 1
        cart_item.save()
    
    if cart_item.item_qty == 0:
        cart_item.delete()

    return JsonResponse({'quantity': cart_item.item_qty, 'code': 'ok'})

def delete_cart_view(request, cart_item_id):
    template_name = 'cart/cart.html'
    user_cart = Cart.objects.get(user=request.user)
    try:
        cart_item = CartItem.objects.get(cart=user_cart, saved_item__id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        raise Http404("Cart item does not exist.")
    return render(request, template_name)
