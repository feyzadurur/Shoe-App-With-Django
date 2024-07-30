from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('shoestore.urls')),
    path('account/',include('authentication.urls')),
    #path('api/',include('authentication.urls')),
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('admin/', admin.site.urls),
]
