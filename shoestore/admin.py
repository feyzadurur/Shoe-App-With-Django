from django.contrib import admin
from .models import Shoe,Cart,CartItem

# Register your models here.

@admin.register(Shoe)
class ShoesAdmin(admin.ModelAdmin):
    list_display=("title","isActive","isHome","gender","category","bestseller","size",)
    list_display_links=("title",)
    list_filter=("title","isActive","isHome","gender","category","bestseller",)
    list_editable=("isActive","isHome",)
    
admin.site.register([Cart,CartItem])