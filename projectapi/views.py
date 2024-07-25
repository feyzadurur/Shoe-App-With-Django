from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializer import UserSerializer
from rest_framework import status


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class Home(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        content={'message': 'Hello, World!'}
        return Response(content)

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
  
  
#idye göre sayfa
# localhost/books  => GET, POST
# localhost/books/2  => GET, PUT, DELETE
@api_view(['GET','PUT','DELETE'])        
def user(request,id):
    try:
        user=User.objects.get(pk=id)
    except:
        return Response({"Eşleşen bir kayıt bulunamadı."},status=status.HTTP_404_NOT_FOUND)
    
    if request.method=="GET":
        serializer=UserSerializer(user) 
        return Response(serializer.data)
    
    elif request.method=="PUT":
        serializer=UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method=="DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    