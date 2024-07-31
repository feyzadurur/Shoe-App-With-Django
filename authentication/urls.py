from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from . views import RegisterView,LoginView,UserView,Home,LogoutView,ChangePasswordView


urlpatterns = [
    path('api/',Home.as_view()),
    path('api/login/',LoginView.as_view()),
    path('api/register/',RegisterView.as_view()),
    path('api/login/user/',UserView.as_view()),
    path('api/login/logout/',LogoutView.as_view()),
    path('api/login/change-password',ChangePasswordView.as_view()),
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]
