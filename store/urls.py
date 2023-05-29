from django.urls import path
from store.views import *

#
app_name = 'store'
urlpatterns = [
    path('', index, name='index'),
    path('subcategory/<int:pk>/', subcategory, name='subcategory'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('contact/', contact, name='contact'),
    path('search/', search_products, name='search'),
    path('products-service/', products_service, name='products_service')
]
