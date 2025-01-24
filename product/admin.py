from django.contrib import admin
from product.models import Product, Variation

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ VariationInline ]
    list_display = 'id', 'name', 'marketing_price', 'product_type',
    list_display_links = 'id',
    search_fields = 'id', 'name',
    list_per_page = 10
    ordering = '-id',
    #prepopulated_fields = { 'slug': ('name',),}
    
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'marketing_price',
    list_display_links = 'id',
    search_fields = 'id', 'name',
    list_per_page = 10
    ordering = '-id',
    
