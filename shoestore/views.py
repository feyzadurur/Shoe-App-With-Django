from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Shoe,Category,Cart, CartItem
from rest_framework.decorators import api_view,action
from django.contrib.auth.decorators import login_required
from .serializer import ShoesSerializer,CartItemSerializer,CategorySerializer

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


#Çok satanlar listesi
@api_view(['GET'])
def bestseller_list(request):
    bestsellers = Shoe.get_bestsellers()
    shoe_serializer = ShoesSerializer(bestsellers, many=True)
    return Response(shoe_serializer.data)

#Sepete ürün ekleme çıkarma
class CartItemModelViewSet(ModelViewSet):
    serializer_class=CartItemSerializer
    queryset=CartItem.objects.all()
    
    @action(detail=False, methods=['GET'])
    def cartitem_quantity(self,request):
        shoe_id=request.query_params.get("shoe_id")
        cart_id=request.query_params.get("cart_id")
        
        try:
            cartitem=CartItem.objects.get(shoe_id=shoe_id,cart_id=cart_id)
            quantity=cartitem.quantity
            return Response (quantity)
        except:
            quantity=0
            return Response(quantity)
            
    
    
    @action(detail=True, methods=['PATCH'])
    def update_item(self,request,pk):
        try:
            cartitem=self.get_object()
            quantity=int(request.data.get("quantity",0))
            if quantity >=1:
                cartitem.quantity=quantity
                cartitem.save()
                serializer=CartItemSerializer(cartitem)
                return Response ({"data":serializer.data,"message":"Cartitem başarıyla güncellendi."})
            else:
                cartitem.delete()
                return Response({'message': 'Item silindi çünkü miktar birden az.'},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
            
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
            return Response({"data": serializer.data , "message":"Cartitem başarıyla oluşturuldu."})
        
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_400_BAD_REQUEST)
               
        
@api_view(['GET'])
def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q=request.GET["q"]
        ayakkabilar=Shoe.objects.filter(isActive=True,title__contains=q).order_by("title")
        
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
        
        response_data = {
            'shoes': shoes_serializer.data,
        }
    else:
        
        return HttpResponse("Ürün Bulunamadı")
    
    return Response(response_data)



#Seçili kategorideki ayakkabilarin gelmesi
@api_view(['POST','GET'])
def getShoesByCategory(request):
    """{
    "category":"spor"
    }"""
    if request.method == 'POST':
        category_name = request.data.get('category')
        if not category_name:
            return Response({'error': 'Category ismi gerekli'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        category_name = request.query_params.get('category')
        if not category_name:
            return Response({'error': 'Category ismi gerekli'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        shoes = Shoe.objects.filter(category=category_name, isActive=True)  # Alan adı isActive
        serializer = ShoesSerializer(shoes, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    
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