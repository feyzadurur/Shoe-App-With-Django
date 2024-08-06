from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.user_login, name='login'),
    path('register/',views.user_register, name='register'),
    path('login/user/',views.getUser, name='user'),
    path('login/logout/',views.user_logout, name='login'),
    path('login/change-password/',views.user_change_password,name='change_password'),
    
    path('yonetici/', views.admin_dashboard, name='admin_dashboard'),
    path('yonetici/login/', views.admin_login, name='admin_login'),
    path('yonetici/logout/', views.admin_logout, name='admin_logout'),
    path('yonetici/password-change', views.admin_password_change, name='admin_password_change'),
    
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]
