from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginUserForm,NewUserForm
from django.http import HttpResponse

# Create your views here.

def user_login(request):
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
                    return HttpResponse("if 1")
                else:
                    return redirect(nextUrl)
            else:
                return HttpResponse("else 1")
        else:
            return HttpResponse("else 2")
    else:
        form=LoginUserForm()
        return HttpResponse("else 3")
    
    
    
def user_register(request):
    if request.method== "POST":
        form=NewUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password1"]
            
            user=authenticate(request, username=username, password=password)
            login(request,user)
            return HttpResponse("Kayıt1")
        else:
            return HttpResponse("Kayıt 2")
    else:
        form=NewUserForm()
        return HttpResponse("Kayıt 3")
    
def change_password(request):
    pass 


    
def user_logout(request):
    messages.add_message(request,messages.SUCCESS,"Çıkış Başarılı")
    logout(request)
    return HttpResponse("Logout")