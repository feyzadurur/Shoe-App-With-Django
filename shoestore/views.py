from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Shoes,Category,Gender
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
    
def shopping_cart(request):
    pass



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


#Cİnsiyete göre kategorideki ayakkabilar gelmesi
@api_view(['GET'])
def getShoesByCategory(request):
    
    gender = request.query_params.get('gender', None)
    category_name = request.query_params.get('category', None)
    
    # Eğer gender bilgisi yoksa hata döndürülüyor
    if gender is None:
        return Response({"error": "Gender parameter is required."}, status=400)

    if not category_name:
        return Response({"error": "Category parameter is required."}, status=400)


    try:
        # Belirli bir kategoriyi adı ile bul
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=404)


    if gender in ['M', 'F'] and category :
        ayakkabilar=Shoes.objects.filter(isActive=True,gender=gender,categories=category).order_by('title')
        kategoriler=Category.objects.filter(gender=gender)
        
        
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
        categories_serializer = CategorySerializer(kategoriler, many=True)

        response_data = {
            'shoes': shoes_serializer.data,
            #'categories': categories_serializer.data
        }
    
        return Response(response_data)
    
    else:
        return Response({"error": "Invalid gender parameter. Use 'M' for Male or 'F' for Female."}, status=400)
    
    """
    return render(request,{
        'categories': kategoriler,
        'shoes': ayakkabilar
    })"""
    
    """
    http://127.0.0.1:8000/category/?gender=M
    http://127.0.0.1:8000/category/?gender=F
    """
    
    
    
#cinsiyete göre ayakkabı filtrelemesi yapiyorr => Tüm ayakkabilar geliyor    
@api_view(['GET'])    
def getShoesByGender(request):
    
    # response_data'dan cinsiyet bilgisi alınıyor
    response_data = {
        'gender': request.query_params.get('gender', None)
    }
    
    gender = response_data.get('gender', None)
    
    # Eğer gender bilgisi yoksa hata döndürülüyor
    if gender is None:
        return Response({"error": "Gender parameter is required."}, status=400)

    
    # Cinsiyet bilgisine göre ayakkabılar filtreleniyor
    if gender in ['M', 'F']:
        ayakkabilar=Shoes.objects.filter(isActive=True,gender=gender).order_by('title')
    
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
    
        return Response(shoes_serializer.data)
    
    else:
        return Response({"error": "Invalid gender parameter. Use 'M' for Male or 'F' for Female."}, status=400)
    
    
    """ Bu url ile cinsiyete göre ayakkabı filtrelemesi yapiyorr
    http://127.0.0.1:8000/filter/?gender=M
    http://127.0.0.1:8000/filter/?gender=F
    """