from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('shoe-add/',views.shoe_add),
    path('shoe-list/',views.shoe_list),
    path('search/',views.search),
    path('add-to-shoppingcart/',views.add_to_shopping_cart),
    path('shopping-cart/',views.shopping_cart_detail,name='shopping_cart_detail',),
    path('category/',views.getShoesByCategory),
    path('filter/',views.getShoesByGender),
]
