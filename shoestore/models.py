from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Gender(models.TextChoices):
    
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'

class Category(models.TextChoices):
    SPOR= "Spor Ayakkabı"
    BOT="Bot"
    TERLIK="Terlik"
    SANDALET="Sandalet"
    TOPUKLU="Topuklu Ayakkabı"
    KLASIK="Klasik Ayakkabı"
   

class Shoe(models.Model):
    title=models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Category.choices,)
    gender = models.CharField(max_length=6, choices=Gender.choices,)
    size = models.CharField(max_length=2)
    description=models.CharField(max_length=255,default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image=models.ImageField(default="")
    bestseller=models.BooleanField(default=False)
    isActive=models.BooleanField(default=True)
    isHome=models.BooleanField(default=True)
    slug=models.SlugField(default="",blank=True,null=False,unique=True,db_index=True)
    
    def __str__(self):
        return f"{self.title} , {self.size}"
    
    
    def save(self, *args, **kwargs):
    
        combined_string = f"{self.title} {self.gender}{self.size}"
        self.slug = slugify(combined_string)
        
       
        super().save(*args,**kwargs)
        
    @classmethod
    def get_bestsellers(cls):
        return cls.objects.filter(bestseller=True, isActive=True)

class Cart(models.Model):
    session_key=models.CharField(max_length=50)
    
    def __str__(self):
        return self.session_key
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.shoe.title}"