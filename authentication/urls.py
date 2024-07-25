from django.urls import path
from . import views
from . views import RegisterView,LoginView,UserView,LogoutView


urlpatterns = [
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('user/',UserView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('change-password',views.change_password,name="change_password"),
    path('logout/',views.user_logout),
]
