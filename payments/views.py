from ast import Or
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from store_main.models import Item
from cart.models import CartItem
from .models import OrderDetailItem

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


class CheckoutSessionview(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        order_item = Item.objects.get(pk=self.kwargs['pk'])
        cart_item = CartItem.objects.get(
            cart__user=request.user, saved_item__id=order_item.id)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(order_item.price*100),
                            'product_data': {
                                'name': order_item.title,
                                # 'images': [item_img]
                            }
                        },
                        'quantity': cart_item.item_qty

                    },

                ],
                metadata={
                    'product': order_item.id,
                    'user': request.user.id
                },
                mode='payment',
                success_url=YOUR_DOMAIN + 'payments/success/',
                cancel_url=YOUR_DOMAIN + 'payments/cancel/',
            )
        except Exception as e:
            raise e

        return redirect(checkout_session.url, code=303)

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs['pk'])
        context = {}
        context['item'] = item
        return render(request, 'payments/checkout.html', context)


class PaymentSuccessView(TemplateView):
    template_name = "payments/payment_success.html"


class PaymentCancelView(TemplateView):
    template_name = "payments/payment_cancel.html"

class OrderSuccessView(ListView):
    template_name = 'payments/orders_view.html'
    model = OrderDetailItem
    context_object_name = 'order_items'
    def get_queryset(self):
        return OrderDetailItem.objects.filter(user_id=self.request.user.id).order_by('-date_created')


endpoint_secret = settings.WHSEC_SECRET

@csrf_exempt
def my_webhook_view(request):
    payload = request.body

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Passed signature verification
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session['customer_details']['email']
        product_id = session['metadata']['product']
        user_id = session['metadata']['user']

        # fulfill order
        complete_order(user_id, customer_email, product_id)

    return HttpResponse(status=200)

def complete_order(user_id, customer_email, product_id):
    # clean up cart
    print(user_id, customer_email, product_id)
    try:
       cart_item = CartItem.objects.get(cart__user__id=user_id, saved_item__id=product_id)
       cart_item.delete()
    except CartItem.DoesNotExist as e:
        # invalid user or cart item.
        raise Http404("Bad request")

    
    # create a new order
    new_order = OrderDetailItem(user_id=user_id, order_email=customer_email, product_id=product_id)
    new_order.save()
    print("New order created")
    
