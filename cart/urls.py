from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartListView.as_view(), name='cart_list'),
    path('update-cart/', views.update_cart_view, name='cart_update'),
]