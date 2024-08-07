
from django.urls import path
from . views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', HomePage.as_view(), name='index'),
   path('about/', About.as_view(), name='about'),
   path('contact/', Contact.as_view(), name='contact'),
   path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
   path('category/<slug:category_slug>/', ShowCategory.as_view(), name='category'),
   path('products/', Products.as_view(), name='products'),
   path("search/", Search.as_view(), name='search'),


]