from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):
        
    name=serializers.CharField(max_length=50)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    
    
class ShoesSerializer(serializers.Serializer):
    
    id=serializers.IntegerField(read_only=True)
    gender = serializers.CharField(max_length=6)
    title=serializers.CharField(max_length=255)
    size = serializers.DecimalField(max_digits=3, decimal_places=1)
    description=serializers.CharField(default="")
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock =serializers.IntegerField()
    image=serializers.ImageField(default="")
    isActive=serializers.BooleanField(default=True)
    isHome=serializers.BooleanField(default=True)
    
    #category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    #category eklenmedi





"""from shoestore.models import Shoes, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'gender']

class ShoesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Shoes
        fields = [
            'id',
            'gender',
            'title',
            'size',
            'description',
            'price',
            'stock',
            'image',
            'isActive',
            'isHome',
            'category'
        ]
    """