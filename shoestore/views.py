from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Shoes,Category
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

from .serializer import ShoesSerializer,CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def index(request):
    if request.method=="GET":
        ayakkabilar=Shoes.objects.filter(isActive=1,isHome=1)
        kategoriler=Category.objects.all()
        
        
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
        categories_serializer = CategorySerializer(kategoriler, many=True)

        response_data = {
            'shoes': shoes_serializer.data,
            'categories': categories_serializer.data
        }

    return Response(response_data)
        
    """
    return render(request,{
        'categories': kategoriler,
        'shoes': ayakkabilar
    })
    """
    
@api_view(['GET'])
#@login_required()
def shoes_list(request):
    ayakkabilar=Shoes.objects.all()
    
    shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
    response_data = {
        'shoes': shoes_serializer.data
    }
    
    return Response(response_data)
    
    """
    return render(request,{
        'shoes': ayakkabilar
    })
    """



@api_view(['GET'])
def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q=request.GET["q"]
        ayakkabilar=Shoes.objects.filter(isActive=True,title__contains=q).order_by("title")
        kategoriler=Category.objects.all()
        
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
        categories_serializer = CategorySerializer(kategoriler, many=True)

        response_data = {
            'shoes': shoes_serializer.data,
            'categories': categories_serializer.data
        }
        
    else:
        #return redirect("/shoes")
        return HttpResponse("TAMAM")
    
    return Response(response_data)

    """
    return render(request,{
        'categories': kategoriler,
        'shoes': ayakkabilar
    })
    """
    
@api_view(['GET'])    
def details(request,slug):
    ayakkabilar=get_object_or_404(Shoes)
    
    #shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
    
    context={
        'shoes': ayakkabilar
    }
    
    return Response(context)



@api_view(['GET'])
def getShoesByCategory(request,slug):
    ayakkabilar=Shoes.objects.filter(isActive=True).order_by('title')
    kategoriler=Category.objects.all()
    
    
    shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
    categories_serializer = CategorySerializer(kategoriler, many=True)

    response_data = {
        'shoes': shoes_serializer.data,
        'categories': categories_serializer.data
    }
    
    return Response(response_data)
    
    """
    return render(request,{
        'categories': kategoriler,
        'shoes': ayakkabilar
    })"""
    