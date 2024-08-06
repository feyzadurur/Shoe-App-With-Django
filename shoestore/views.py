from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Shoe,Category,Cart, CartItem,Gender
from rest_framework.decorators import api_view,action
from django.contrib.auth.decorators import login_required
from .serializer import ShoesSerializer,CartItemSerializer,CategorySerializer,GenderSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def index(request):
   
    if request.method=="GET":
        ayakkabilar=Shoe.objects.filter(isActive=1,isHome=1)     
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)  
        response_data = {
            'shoes': shoes_serializer.data,
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
    
    def get_response_data(self, data):
        return {"cart": data}
    
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
               
class SearchView(APIView):
    def get(self, request):
        gender = request.query_params.get('gender')
        title = request.query_params.get('title')
        category = request.query_params.get('category')

        filters = Q()
        
        if gender:
            filters &= Q(gender=gender)
        
        if title:
            filters &= Q(title__icontains=title)
        
        if category:
            filters &= Q(category=category)

        shoes = Shoe.objects.filter(filters)
        shoe_serializer = ShoesSerializer(shoes, many=True)

        return Response(shoe_serializer.data, status=status.HTTP_200_OK)
    
"""    
#Gender, Title, Category araması yaparak sonuçları getiriyor        
@api_view(['GET'])
def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q=request.GET["q"]
        ayakkabilar=Shoe.objects.filter(isActive=True,title__contains=q).order_by("title","gender","category")
        shoes_serializer = ShoesSerializer(ayakkabilar, many=True)
        response_data = {
            'shoes': shoes_serializer.data,
        }
        return Response(response_data)
    else:
        return Response({'message': 'Ürün bulunamadı.'},status=status.HTTP_204_NO_CONTENT)
 """   


#Sadece category bilgileri
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.choices
        category_list = [{'value': choice[0],} for choice in categories]
        category_serializer = CategorySerializer(category_list, many=True)
        
        response_data = {
            'value': category_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


#categorye göre ayakkabı filtrelemesi yapiyorr => Tüm ayakkabilar geliyor
class GetShoesByCategory(APIView):
    def get(self, request):     
        
        category_name = request.query_params.get('category')
        if not category_name:
            return Response({'error': 'Category ismi gerekli'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            shoes = Shoe.objects.filter(category=category_name, isActive=True)  # Alan adı isActive
            serializer = ShoesSerializer(shoes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """ Bu url ile kategoriye göre ayakkabı filtrelemesi yapiyorr
    http://127.0.0.1:8000/filter/?category=Spor%20Ayakkabı
    http://127.0.0.1:8000/filter/?category=Topuklu%20Ayakkabı
    """
   

#cinsiyete göre ayakkabı filtrelemesi yapiyorr => Tüm ayakkabilar geliyor 
class GetShoesByGender(APIView):  
    def get(self, request): 
        
        gender= Gender.choices
        gender_list = [{'cinsiyet': choice[0],} for choice in gender]
        gender_serializer = GenderSerializer(gender_list, many=True)
        
        
        gender_param = request.query_params.get('gender')
         
        # Eğer gender bilgisi yoksa hata döndürülüyor
        if gender is None:
            return Response({"error": "Gender parametresi gerekli"}, status=status.HTTP_400_BAD_REQUEST)


        # Cinsiyet bilgisine göre ayakkabılar filtreleniyor
        shoes = Shoe.objects.filter(gender=gender_param)
        shoe_serializer = ShoesSerializer(shoes, many=True)
        
        return Response(shoe_serializer.data, status=status.HTTP_200_OK)
    """Bu url ile cinsiyete göre ayakkabı filtrelemesi yapiyorr
    http://127.0.0.1:8000/filter/?gender=M
    http://127.0.0.1:8000/filter/?gender=F
    """
    
