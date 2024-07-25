from django.urls import path
from . import views

urlpatterns = [
    path('',views.users),
    path('<int:id>',views.user),
]
