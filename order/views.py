from django.shortcuts import render
from django.views.generic import View, DetailView
from order.models import Order

class PaymentView(View):
    pass

class CloseOrderView(View):
    pass

class OrderDetailView(DetailView):
    model = Order
    template_name = 'CHANGE-ME'
    context_object_name = 'order'
    
    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs.get('pk'))



