from django.urls import path, include
from product import views

app_name = 'product'

urlpatterns = [
    path('', include(views.ProductListView.as_view()), name='list'),
    path('<slug:slug>/', include(views.ProductDetailView.as_view()), name='detail'),
    path('addtocart/', include(views.AddToCartView.as_view()), name='addtocart'),
    path('removefromcart/', include(views.RemoveFromCartView.as_view()), name='removefromcart'),
    path('cart/', include(views.CartView.as_view()), name='cart'),
    path('finish/', include(views.FinishView.as_view()), name='finish'),
]