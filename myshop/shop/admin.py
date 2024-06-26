from django.contrib import admin
from django.http import HttpRequest
from .models import Category, Product
from parler.admin import TranslatableAdmin

# Register your models here.
@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    #prepopulated_fields = {'slug': ('name',)} отпадает необходимость, из-за перевода
    
    def get_prepopulated_fields(self, request, obj = None):
        return {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    #prepopulated_fields = {'slug': ('name',)}

    def get_prepopulated_fields(self, request, obj = None):
        return {'slug': ('name',)}