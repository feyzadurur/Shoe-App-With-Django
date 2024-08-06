from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .serializer import UserSerializer, ChangePasswordSerializer
from .models import User 
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from datetime import datetime,timedelta 

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.backends import BaseBackend

from django.contrib.auth.decorators import login_required,permission_required
from .forms import AdminPasswordChangeForm, AdminLoginForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash

from rest_framework.decorators import api_view, permission_classes
# Create your views here.


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:  # Kullanıcının admin yetkisine sahip olup olmadığını kontrol et
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, 'Geçersiz kullanıcı adı veya şifre')
    else:
        form = AdminLoginForm()
    return render(request, 'admin/login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
def admin_password_change(request):
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Şifre değiştirdikten sonra kullanıcıyı oturumdan atma
            return redirect('admin:password_change_done')
    else:
        form = AdminPasswordChangeForm(user=request.user)
        return render(request, 'admin/password_change_form.html', {'form': form})
    
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    return render(request, 'admin/dashboard.html')
    
    
"""
"first_name":"feyza",
"last_name":"durur",
"email":"fdurur@gmail.com",
"username":"fdd",
"password":"fd1234"

}"""


@api_view(['POST','GET'])
def user_register(request):
    if request.method=="GET":
        users=User.objects.all()
        serializer=UserSerializer(users, many=True)   
        return Response(serializer.data)
    
    if request.method=="POST":
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    
        
    """
        {
        "username":"fd",
        "password":"fd123"
        }
    """
    
@api_view(['POST','GET'])    
def user_login(request):     
    if request.method == 'POST':
        username=request.data['username']
        password=request.data['password']
        
        user=User.objects.filter(username=username).first()
        
        if user is None:
            raise AuthenticationFailed('Kullanıcı bulunamadı!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Şifre yanlış!')
       
        payload={
            'id' : user.id,
            'exp' : datetime.utcnow() + timedelta(minutes=60),
            'iat' : datetime.utcnow()
        }
        
        
        #Decode encode değiştirildi
        
        token=jwt.encode(payload,'secret')
        
        token_string=jwt.decode(token,'secret',algorithms=['HS256'])
        
        response= Response()
        
        response.set_cookie(key='jwt',value=token_string,httponly=True)
        
        response.data ={
            'jwt':token_string
            
        }

        
        return response
    
    if request.method == 'GET':
        token=request.COOKIES.get('jwt')     
            
        if not token:
            raise AuthenticationFailed('Giriş yapılmadı!')  
            
        try:
            payload=jwt.decode(token,'secret', algorithms=['HS256'])    
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Giriş yapılmadı!')
                                        
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)
        return Response(serializer.data)
        
  
   
     
@api_view(['GET'])       
def getUser(request):
    token=request.COOKIES.get('jwt')     
        
    if not token:
        raise AuthenticationFailed('Unauthenticated!')  
    
    try:
        payload=jwt.decode(token,'secret', algorithms=['HS256'])    
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Giriş Yapılmadı!')
        
    user=User.objects.filter(id=payload['id']).first()
    serializer=UserSerializer(user)
    return Response(serializer.data)
        
    
    
@api_view(['POST']) 
#kendi decaratorüm gelecek
def user_logout(request):
    if request.method=="POST":
        username=request.data['username']
        password=request.data['password']
        #id=request.data['id']
            
        user=User.objects.filter(username=username).first()
        #user=User.objects.get(pk=id)
            
        if user is None:
            raise AuthenticationFailed('User not found!')
            
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
            
        logout(request)
        response=Response()
        response.delete_cookie('jwt')
        response.data={
                
            'message': 'success'
        }
            
        return response
    
        
        
    

@api_view(['GET']) 
def home(request):
    content={'message': 'Hello, World!'}
    return Response(content)


@api_view(['POST']) 
def user_change_password(request):   
    """{ 
    "old_password":"fd123",
    "new_password1":"fd1234",
    "new_password2":"fd1234"
    }
    """    
    if request.method=="POST":
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password1']
            
            if not user.check_password(old_password):
                return Response({"old_password": ["Şifre Yanlış."]}, status=status.HTTP_400_BAD_REQUEST)
            
            if old_password == new_password:
                return Response({"new_password": ["Yeni şifre eski şifre ile aynı olamaz."]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
           
            return Response({"detay": "Parola değiştirildi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

 