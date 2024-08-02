from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from . views import RegisterView,LoginView,UserView,Home,LogoutView,ChangePasswordView


urlpatterns = [
    path('',Home.as_view()),
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('login/user/',UserView.as_view()),
    path('login/logout/',LogoutView.as_view()),
    path('login/change-password',ChangePasswordView.as_view()),
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]
