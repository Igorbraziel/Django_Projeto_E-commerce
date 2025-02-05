from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_value = models.FloatField()
    total_quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        default='C', max_length=1,
        choices=(
            ('A', 'approved'),
            ('C', 'created'),
            ('D', 'disapproved'),
            ('P', 'pending'),
            ('S', 'shipped'),
            ('F', 'finished'),
        )
    )    
    
    def __str__(self):
        return f'Order Nº. {self.pk}'
    
    
class OrderItem(models.Model):
    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation_name = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image_url = models.CharField(max_length=2000)
    
    def __str__(self):
        return f'Item of {self.order}'
