from django.urls import path
from product import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('addtocart/', views.AddToCartView.as_view(), name='addtocart'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('removefromcart/', views.RemoveFromCartView.as_view(), name='removefromcart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('finish/', views.FinishView.as_view(), name='finish'),
]