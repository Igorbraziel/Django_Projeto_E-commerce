from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from product.models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'
    ordering = '-pk',
    context_object_name = 'products'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
    
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'CHANGE-ME'
    ordering = '-pk',
    context_object_name = 'product_obj'
    slug_field = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(slug=self.kwargs.get('slug'))
    
    
class AddToCartView(View):
    pass

class RemoveFromCartView(View):
    pass

class CartView(View):
    pass

class FinishView(View):
    pass
    
