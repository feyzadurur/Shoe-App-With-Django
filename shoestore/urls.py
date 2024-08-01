from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("cartitems",views.CartItemModelViewSet)

urlpatterns = [
    path('',views.index),
    path('cart/',include(router.urls)),
    path('bestseller/', views.bestseller_list),
    path('shoe-add/',views.shoe_add),
    path('shoe-list/',views.shoe_list),
    path('search/',views.search),
    path('category/',views.getShoesByCategory),
    path('filter/',views.getShoesByGender),
]
