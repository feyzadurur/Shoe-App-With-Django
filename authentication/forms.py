from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm)
from django.forms import widgets
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.models import User

class AdminPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Eski Şifre")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Yeni Şifre")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Yeni Şifre (Tekrar)")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Eski şifre yanlış.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Yeni şifreler eşleşmiyor.")
        return cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user
    
class AdminLoginForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı')
    password = forms.CharField(widget=forms.PasswordInput, label='Şifre')    
    
    
class LoginUserForm(AuthenticationForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget=widgets.TextInput(attrs={"class":"form-control"})
        self.fields["password"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
    def clean_username(self):
        username=self.cleaned_data.get("username")
        
        if username == "admin":
            messages.add_message(self.request,messages.SUCCESS, "hoşgeldin yetkili")
        
        return username
           
           
class NewUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=("username","email","first_name","last_name",)
        #tasarım belirlenince buraya
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        self.fields["password2"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        self.fields["username"].widget=widgets.TextInput(attrs={"class":"form-control"})
        self.fields["email"].widget=widgets.EmailInput(attrs={"class":"form-control"})
        self.fields["first_name"].widget=widgets.TextInput(attrs={"class":"form-control"})
        self.fields["last_name"].widget=widgets.TextInput(attrs={"class":"form-control"})
        self.fields["email"].required=True
        #fieldslar ilgili yerlere
        
        
class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        self.fields["new_password2"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        self.fields["old_password"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        
        