from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('account/',include('authentication.urls')),
    path('api/',include('projectapi.urls')),
    path('admin/', admin.site.urls),
]
