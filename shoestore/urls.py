from django.urls import path,include

from .views import CategoryListView,GetShoesByGender,GetShoesByCategory,SearchView
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("cartitems",views.CartItemModelViewSet)

urlpatterns = [
    path('',views.index),
    path('cart/',include(router.urls)),
    path('bestseller/', views.bestseller_list),
    path('shoe-add/',views.shoe_add),
    path('search/',SearchView.as_view()),
    path('category/',CategoryListView.as_view()),
    path('shoescategory/',GetShoesByCategory.as_view()),
    path('filter/',GetShoesByGender.as_view()),
]
