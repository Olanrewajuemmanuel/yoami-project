from django.urls import path

from . import views

app_name = 'payments'
urlpatterns = [
    path('order/<pk>/', views.CheckoutSessionview.as_view(), name='payment_checkout'),
    path('success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='payment_cancel'),
    path('order-details/', views.OrderSuccessView.as_view(), name='order_details'),
]