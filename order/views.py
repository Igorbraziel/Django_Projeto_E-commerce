from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView
from django.contrib import messages
from django.urls import reverse

from order.models import Order, OrderItem
from product.models import Variation
from utils import my_functions

class DispatchLoginRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile_app:create')
        
        return super().dispatch(request, *args, **kwargs)
    

class PaymentView(DetailView):
    model = Order
    template_name = 'order/payment.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs.get('pk'), user=self.request.user)
        
        

class CloseOrderView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You need to log in')
            return redirect('profile_app:create')
        
        if not self.request.session.get('cart'):
            messages.error(self.request, 'You cart is empty')
            return redirect('product:list')
        
        cart = self.request.session.get('cart')
        
        variations_ids = [variation_id for variation_id in cart]
        
        variations = Variation.objects.filter(id__in=variations_ids).all()
        
        for variation in variations:
            vid = variation.id
            
            if variation.stock < cart[str(vid)]['quantity']:
                cart[str(vid)]['quantity'] = variation.stock
                cart[str(vid)]['quantitative_price'] = cart[str(vid)]['quantity'] * cart[str(vid)]['unit_price']
                cart[str(vid)]['quantitative_promotional_price'] = cart[str(vid)]['quantity'] * cart[str(vid)]['unit_promotional_price']
                
                messages.error(self.request, "We don't have this product quantity in our stock, we put everything we have in your cart")
                self.request.session.save()
                return redirect('product:cart')
            
        cart_total_quantity = my_functions.cart_total_quantity(cart)
        cart_total_value = my_functions.cart_total_value(cart)
        
        order = Order(
            user=self.request.user,
            total_value=cart_total_value,
            total_quantity=cart_total_quantity,
        )
        
        order.save()
        
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product_name=cart_element['product_name'],
                    product_id=cart_element['product_id'],
                    variation_name=cart_element['variation_name'],
                    variation_id=cart_element['variation_pk'],
                    price=cart_element['quantitative_price'],
                    promotional_price=cart_element['quantitative_promotional_price'],
                    quantity=cart_element['quantity'],
                    image_url=cart_element['image_url'],
                ) for cart_element in cart.values()
            ]
        )
        
        del self.request.session['cart']
        
        return redirect(
                        reverse(
                            'order:payment', 
                            kwargs={
                                'pk': order.pk
                            }
                        )
                    )
    

class OrderDetailView(DetailView):
    model = Order
    template_name = 'CHANGE-ME'
    context_object_name = 'order'
    
    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs.get('pk'))
    
class OrderListView(ListView):
    template_name = 'order/list.html'
    model = Order
    context_object_name = 'orders'



