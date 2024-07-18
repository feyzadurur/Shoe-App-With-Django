from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializer import UserSerializer
from rest_framework import status

# Create your views here.

@api_view(['GET','POST'])
def users(request):
    if request.method=="GET":
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)
    if request.method=="POST":
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
  
@api_view(['GET','PUT','DELETE'])        
def user(request,id):
    try:
        user=User.objects.get(pk=id)
    except:
        return Response({"Eşleşen bir kayıt bulunamadı."},status=status.HTTP_404_NOT_FOUND)
        
    