from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages

from django.http import HttpResponse
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
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

# Create your views here.

"""class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
"""

"""{
"first_name":"feyza",
"last_name":"durur",
"email":"fdurur@gmail.com",
"username":"fdd",
"password":"fd1234"

}"""

class RegisterView(APIView):
    authentication_classes = []  # Bu view için kimlik doğrulamayı devre dışı bırak
    #permission_classes = [AllowAny]  # Bu view için izin kontrollerini devre dışı bırak

    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
class LoginView(APIView):
    #authentication_classes = []  # Bu view için kimlik doğrulamayı devre dışı bırak
    #permission_classes = [IsAuthenticated]  # Bu view için izin kontrollerini devre dışı bırak

    """
        {
        "username":"fd",
        "password":"fd123"
        }
    """
      
    def post(self,request):
        
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
        
        token=jwt.encode(payload,'secret',algorithm='HS256')
        #token_string=token.decode('utf-8')
        
        response= Response()
        
        response.set_cookie(key='jwt',value=token,httponly=True)
        
        response.data ={
            'jwt':token
        }

        
        return response
    
    def get(self,request):
        token=request.COOKIES.get('jwt')     
        
        if not token:
            raise AuthenticationFailed('Giriş yapılmadı!1')  
        
        try:
            payload=jwt.decode(token,'secret', algorithms=['HS256'])    
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Giriş yapılmadı!')
                                       
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)
        return Response(serializer.data)
  
    
                
class UserView(APIView) :
    def get(self,request):
        token=request.COOKIES.get('jwt')     
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  
        
        try:
            payload=jwt.decode(token,'secret', algorithms=['HS256'])    
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)
        return Response(serializer.data)
        
        
class LogoutView(APIView):
    authentication_classes = []  # Bu view için kimlik doğrulamayı devre dışı bırak
    permission_classes = [IsAuthenticated]  # Bu view için izin kontrollerini devre dışı bırak

    """ authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
        {
        "username":"fd",
        "password":"fd123"
        }
    
    
    """
    
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        
        user=User.objects.filter(username=username).first()
        
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
        
    

#for postman       
class Home(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        content={'message': 'Hello, World!'}
        return Response(content)


class ChangePasswordView(APIView):
    authentication_classes = []  # Bu view için kimlik doğrulamayı devre dışı bırak
    #permission_classes = [AllowAny]  # Bu view için izin kontrollerini devre dışı bırak

    #permission_classes = [IsAuthenticated,]
    
    """{ 
    "old_password":"fd123",
    "new_password1":"fd1234",
    "new_password2":"fd1234"
    }
    """    
    
    def post(self,request, *args, **kwargs):
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
     

 