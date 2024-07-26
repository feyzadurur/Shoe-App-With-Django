from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('shoe-list/',views.shoes_list),
    path('search/',views.search),
    path('details/',views.details),
    path('category/',views.getShoesByCategory),
    path('filter/',views.getShoesByGender),
]
