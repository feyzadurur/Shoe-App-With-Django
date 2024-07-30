from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginUserForm,NewUserForm,UserPasswordChangeForm
from django.http import HttpResponse
from .serializer import UserSerializer
from .models import User 
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from datetime import datetime,timedelta 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
# Create your views here.

"""{
"first_name":"feyza",
"last_name":"durur",
"email":"fdurur@gmail.com",
"username":"fdd",
"password":"fd1234"

}"""

class RegisterView(APIView):
 
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    """def user_register(request):
    if request.method== "POST":
        form=NewUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password1"]
            
            user=authenticate(request, username=username, password=password)
            login(request,user)
            return HttpResponse("Kayıt1") #Anasayfaya yönlendir
        else:
            return HttpResponse("Kayıt 2") #Registere yönlendir
    else:
        form=NewUserForm()
        return HttpResponse("Kayıt 3") #Registere yönlendir

    """
    
    
class LoginView(APIView):
    """
        {
        "username":"fd",
        "password":"fd123"
        }
    """
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
    
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        
        user=User.objects.filter(username=username).first()
        
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        #if request.user.is_authenticated and "next" in request.GET:
        #   return render(request,messages.SUCCESS,"Deneme")
        
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
    
    
        
    """@api_view(['POST']) 
    def user_login(self,request):
        if request.user.is_authenticated and "next" in request.GET:
            return render(request,messages.SUCCESS,"Deneme")
        if request.method=="POST":
            form=LoginUserForm(request,data=request.POST)
            if form.is_valid():
                username=form.cleaned_data.get("username")
                password=form.cleaned_data.get("password")
                
                user=authenticate(request,username=username,password=password)
                
                if user is not None:
                    login(request,user)
                    messages.add_message(request,messages.SUCCESS,"Giriş Başarılı")
                    nextUrl=request.GET.get("next",None)
                    if nextUrl is None:
                        return HttpResponse("if 1") #Anasayfaya yönlendir
                    else:
                        return redirect(nextUrl)
                else:
                    return HttpResponse("else 1") #Logine yönlendir
            else:
                return HttpResponse("else 2")#Logine yönlendir
        else:
            form=LoginUserForm()
            return HttpResponse("else 3")#Logine yönlendir
        """
    
                
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
    def post(self,request):
        
        username=request.data['username']
        password=request.data['password']
        
        user=User.objects.filter(username=username).first()
        
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        #messages.add_message(request,messages.SUCCESS,"Çıkış Başarılı")
        
        logout(request)
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            
            'message': 'success'
        }
        
        return response
        
    """   
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message': 'success'
        }
        
        return response
    def user_logout(request):
    messages.add_message(request,messages.SUCCESS,"Çıkış Başarılı")
    logout(request)
    return HttpResponse("Logout") #Anasayfaya yönlendir"""

#for postman       
class Home(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        content={'message': 'Hello, World!'}
        return Response(content)

class ChangePasswordView(APIView):
    
    def post(self,request):
        pass
    def change_password(request):
        if request.method=="POST":
            form=UserPasswordChangeForm(request.user,request.POST)
            if form.is_valid():
                user=form.save()
                update_session_auth_hash(request,user)
                messages.success(request,"Parola güncellendi.")
                return redirect("change_password")
            else:
                return render(request,{"form":form}) #Parola değiştirme ekranına yönlendir
        form=UserPasswordChangeForm(request.user)
        return render(request,{"form":form})#Parola değiştirme ekranına yönlendir


 