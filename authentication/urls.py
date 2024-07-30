from django.urls import path

from . views import RegisterView,LoginView,UserView,Home,LogoutView,ChangePasswordView


urlpatterns = [
    path('home/',Home.as_view()),
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('user/',UserView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('change-password',ChangePasswordView.as_view())
    #path('logout/',views.user_logout),
]
