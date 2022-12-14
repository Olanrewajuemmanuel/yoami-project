from . import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store_main'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('search/', views.search_detail, name="search"),
    path('details/<int:pk>/', views.ItemDetailView.as_view(), name="item_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

