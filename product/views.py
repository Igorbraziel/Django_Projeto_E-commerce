from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from product.models import Product, Variation
from profile_app.models import UserProfile

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
    template_name = 'product/detail.html'
    context_object_name = 'product_obj'
    slug_field = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(slug=self.kwargs.get('slug'))
    
    
class AddToCartView(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('product:list'))
        variation_id = self.request.GET.get('vid')
        
        if not variation_id:
            messages.error(
                self.request,
                "Product doesn't exists"
            )
            return redirect(http_referer)
        
        variation = get_object_or_404(Variation, id=variation_id)
        
        if variation.stock < 1:
            messages.error(
                self.request,
                'Insufficient stock'
            )
            return redirect(http_referer)
        
        product_id = variation.product.pk
        product_name = variation.product.name
        variation_name = variation.name
        variation_pk = variation.pk
        unit_price = variation.marketing_price
        unit_promotional_price = variation.marketing_promotional_price
        quantity = 1
        slug = variation.product.slug
        image_url = None
        
        if variation.product.image:
            image_url = variation.product.image.url   
        
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()
            
        cart = self.request.session['cart']
        
        if variation_id in cart:
            cart_quantity = cart[variation_id]['quantity']
            if cart_quantity + 1 > variation.stock:
                messages.warning(self.request, 'Insufficient stock')
                return redirect(http_referer)
            cart_quantity += 1
            cart[variation_id]['quantity'] = cart_quantity
            cart[variation_id]['quantitative_price'] = unit_price * cart_quantity
            cart[variation_id]['quantitative_promotional_price'] = unit_promotional_price * cart_quantity
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_pk': variation_pk,
                'unit_price': unit_price,
                'unit_promotional_price': unit_promotional_price,
                'quantitative_price': unit_price,
                'quantitative_promotional_price': unit_promotional_price,
                'quantity': quantity,
                'slug': slug,
                'image_url': image_url,
            }
            
        self.request.session.save()
        
        messages.success(self.request, 'Product add to cart!')
        
        return redirect(http_referer)

class RemoveFromCartView(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('product:list'))
        variation_id = self.request.GET.get('vid')
        cart = self.request.session.get('cart')
        
        if not variation_id or not cart or not variation_id in cart:
            return redirect(http_referer)
        
        messages.success(self.request, f'{cart[variation_id]["product_name"]} - Removed from cart')
        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(http_referer)
        

class CartView(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart')
        }
        return render(
            self.request,
            'product/cart.html',
            context=context
        )

class PurchaseSummaryView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile_app:create')
        
        profile_exists = UserProfile.objects.filter(user=self.request.user)
        
        if not profile_exists:
            messages.error(self.request, 'User without Profile')
            return redirect('profile_app:create')
        
        if not self.request.session.get('cart'):
            messages.error(self.request, 'Your cart is empty')
            return redirect('product:list')
        
        context = {
            'user': self.request.user,
            'cart': self.request.session.get('cart'),
        }
        
        return render(self.request, 'product/purchasesummary.html', context)
    
    
class SearchView(ProductListView):
    def get_queryset(self):
        search_value = self.request.GET.get('search_value') or self.request.session.get('search_value')
        
        if not search_value:
            return super().get_queryset()
        
        self.request.session['search_value'] = search_value
        
        self.request.session.save()
            
        return super().get_queryset().filter(
            Q(name__icontains=search_value) |
            Q(short_description__icontains=search_value) |
            Q(long_description__icontains=search_value)
        )
    
