from rest_framework import serializers  
from .models import Cart,CartItem,Shoe


class ShoesSerializer(serializers.Serializer):
    """class Meta:
        model= Shoe
        fields=["id","gender","category","title","size","description","price","title","stock","image","isActive","isHome"]"""
    id=serializers.IntegerField(read_only=True)
    gender = serializers.CharField(max_length=6)
    category = serializers.CharField(max_length=20)
    title=serializers.CharField(max_length=255)
    size = serializers.DecimalField(max_digits=3, decimal_places=1)
    description=serializers.CharField(default="")
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock =serializers.IntegerField()
    image=serializers.ImageField(default="")
    isActive=serializers.BooleanField(default=True)
    isHome=serializers.BooleanField(default=True)
 
 
class CartItemSerializer(serializers.ModelSerializer):
    shoe=ShoesSerializer(read_only=True)
    shoe_id=serializers.IntegerField()
    sub_total=serializers.SerializerMethodField()
    class Meta:
        model=CartItem
        fields=["id","shoe","shoe_id","quantity","sub_total"]
        
    def get_sub_total(self, cartitem):
        total_price=cartitem.quantity * cartitem.shoe.price
        return total_price
    
class CartSerializer(serializers.ModelSerializer):
    total_price=serializers.SerializerMethodField()
    total_cartitems=serializers.SerializerMethodField()
    cartitems=CartItemSerializer(read_only=True,many=True)
    class Meta:
        model= Cart
        fields= ["id","sessin_key","total_cartitems","total_price"]
    
    def get_total_price(self, cart): 
        total_price=sum([item.quantity * item.shoe.price for item in cart.cartitems.all()] )
        return total_price
    
    def get_total_cartitems(self, cart): 
        total_cartitems=sum([item.quantity for item in cart.cartitems.all()])
        return total_cartitems