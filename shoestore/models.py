from django.db import models
from django.utils.text import slugify

# Create your models here.

class Gender(models.TextChoices):
    
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'

"""class SizeNo(models.TextChoices):
        otuzalti= '36',
        otuzalti= '36',
        otuzalti= '36',
        otuzalti= '36',
        otuzalti= '36',
        
        ('37', '37'),
    """

    
class Category(models.Model):
    name=models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=Gender.choices,default='Female')
    slug=models.SlugField(default="",null=False,blank=True,unique=True,db_index=True,max_length=50)
    
    
    def save(self, *args, **kwargs):
        combined_string = f"{self.name} {self.gender}"
        self.slug = slugify(combined_string)
        super().save(args,kwargs)
        
    def __str__(self): #url oluşturma
        return f"{self.name},{self.gender}"



class Shoes(models.Model):
    title=models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE),
    gender = models.CharField(max_length=6, choices=Gender.choices,)
    size = models.CharField(max_length=2)
    description=models.CharField(max_length=255,default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image=models.ImageField(default="")
    isActive=models.BooleanField(default=True)
    isHome=models.BooleanField(default=True)
    slug=models.SlugField(default="",blank=True,null=False,unique=True,db_index=True)
    
    categories=models.ManyToManyField(Category)
    
    def __str__(self):
        return f"{self.title} , {self.size}"
    
    
    def save(self, *args, **kwargs):
        """if self.gender == Gender.MALE:
            valid_sizes = [size for size, _ in SizeNo.MALE_SIZES]
        else:
            valid_sizes = [size for size, _ in SizeNo.FEMALE_SIZES]

        if self.size not in valid_sizes:
            raise ValueError("Invalid shoe size for the selected gender")
        
        """
        
        
        combined_string = f"{self.title} {self.gender}"
        self.slug = slugify(combined_string)
        
       
        super().save(*args,**kwargs)
