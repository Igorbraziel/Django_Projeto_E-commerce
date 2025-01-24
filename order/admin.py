from django.contrib import admin
from order.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ OrderItemInline ]
    list_display = 'id', 'total', 'status',
    list_display_links = 'id',
    search_fields = 'id', 'total',
    list_per_page = 10    
    ordering = '-id',
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = 'id', 'product_name', 'price', 'quantity',
    list_display_links = 'id',
    search_fields = 'id', 'product_name',
    list_per_page = 10    
    ordering = '-id',
    

