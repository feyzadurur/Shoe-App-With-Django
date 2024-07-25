from django.contrib import admin
from .models import Shoes,Category

# Register your models here.

@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display=("title","isActive","isHome",)
    list_display_links=("title",)
    list_filter=("title","isActive","isHome",)
    list_editable=("isActive","isHome",)
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=("name",)
    