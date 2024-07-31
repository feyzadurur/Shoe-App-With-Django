from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Shoe,Category,Cart, CartItem
from rest_framework.decorators import api_view,action
from django.contrib.auth.decorators import login_required
from .serializer import ShoesSerializer,CartItemSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def index(request):
    """ anasayfa/ shoes
    anasayfa/ shoe-add/
    anasayfa/ search/
    anasayfa/ add-to-shoppingcart/
    anasayfa/ shopping-cart/ [name='shopping_cart_detail']
    anasayfa/ category/
    anasayfa/ filter/"""
    if request.method=="GET":
        
        ayakkabilar=Shoe.objects.filter(isActive=1,isHome=1)
        #kategoriler=Category.objects.all()
     
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
        #categories_serializer = CategorySerializer(kategoriler, many=True)

        response_data = {
            'shoes': shoes_serializer.data,
            #'categories': categories_serializer.data
        }
    return Response(response_data)
    
@api_view(['POST'])
def shoe_add(request):
    if request.method=="POST":
        shoes_serializer = ShoesSerializer(data=request.data)
        if shoes_serializer.is_valid():
            shoes_serializer.save()
            return Response(shoes_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(shoes_serializer.errors)

@api_view(['GET'])
def shoe_list(request):
    shoes=Shoe.objects.all()
    shoes_serializer=ShoesSerializer(shoes,many=True)
    return Response(shoes_serializer.data)

class CartItemModelViewSet(ModelViewSet):
    serializer_class=CartItemSerializer
    queryset=CartItem.objects.all()
    
    @action(detail=False, methods=["POST"])
    def add_item(self,request):
        try:
            shoe_id=request.data.get("shoe_id")
            
            session_key=request.session.session_key
            if not session_key:
                request.session.save()
                session_key=request.session.session_key
            cart,created=Cart.objects.get_or_create(session_key=session_key)
            cartitem,created=CartItem.objects.get_or_create(shoe_id=shoe_id,cart=cart)
            if not created:
                cartitem.quantity+=1
                cartitem.save()
            else:
                cartitem.quantity=1
                cartitem.save()
                
            serializer =CartItemSerializer(cartitem)
            return Response({"data": serializer.data , "message":"Cartitem created successfully"})
        
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_400_BAD_REQUEST)
               
        
@api_view(['GET'])
def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q=request.GET["q"]
        ayakkabilar=Shoe.objects.filter(isActive=True,title__contains=q).order_by("title")
        #kategoriler=Category.objects.all()
        
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
        #categories_serializer = CategorySerializer(kategoriler, many=True)

        response_data = {
            'shoes': shoes_serializer.data,
        }
    else:
        #return redirect("/shoes")
        return HttpResponse("TAMAM")
    
    return Response(response_data)


@login_required()      
def add_to_shopping_cart(request,shoes_id):
    ayakkabi=get_object_or_404(Shoe,id=shoes_id)
    cart, created = Cart.objects.get_or_create()

    cart_item, created = CartItem.objects.get_or_create(cart=cart, shoe=ayakkabi)
    if not created:
        # Eğer ürün zaten sepetinizde varsa, miktarı arttır
        cart_item.quantity += 1
        cart_item.save()

    return redirect('shopping_cart_detail')

    
@login_required()    
def shopping_cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return Response(context)



#Cinsiyete göre kategorideki ayakkabilar gelmesi
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
        ayakkabilar=Shoe.objects.filter(isActive=True,gender=gender,categories=category).order_by('title')
        kategoriler=Category.objects.filter(gender=gender)
        
        
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
        #categories_serializer = CategorySerializer(kategoriler, many=True)

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
        ayakkabilar=Shoe.objects.filter(isActive=True,gender=gender).order_by('title')
    
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
    
        return Response(shoes_serializer.data)
    
    else:
        return Response({"error": "Invalid gender parameter. Use 'M' for Male or 'F' for Female."}, status=400)
    
    
    """ Bu url ile cinsiyete göre ayakkabı filtrelemesi yapiyorr
    http://127.0.0.1:8000/filter/?gender=M
    http://127.0.0.1:8000/filter/?gender=F
    """