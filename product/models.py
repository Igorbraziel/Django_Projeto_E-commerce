from django.db import models
from utils.images import resize_image
from utils.rands import slugify_new

class Product(models.Model):
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(upload_to='products_images/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(
        unique=True, blank=True, null=True,
        default=None, max_length=255
    )
    marketing_price = models.FloatField()
    marketing_promotional_price = models.FloatField(default=0)
    product_type = models.CharField(
        default='S', max_length=1, 
        choices=(
            ('V', 'variation'),
            ('S', 'simple')
        )
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
            
        super().save(*args, **kwargs)
        
        if self.image:
            self.image = resize_image(self.image)
    
    def __str__(self):
        return self.name
    

class Variation(models.Model):
    class Meta:
        verbose_name = 'variation'
        verbose_name_plural = 'variations'
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    marketing_price = models.FloatField()
    marketing_promotional_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.product.name
        super().save(*args, **kwargs)
    
    def __str__(self):
        if not self.name:
            return self.product.name
        return self.name

