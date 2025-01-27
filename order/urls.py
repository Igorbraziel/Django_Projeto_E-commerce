from django.urls import path, include
from order import views

app_name = 'order'

urlpatterns = [
    path('', include(views.PaymentView.as_view()), name='payment'),
    path('closeorder/', include(views.CloseOrderView.as_view()), name='closeorder'),
    path('detail/<int:pk>/', include(views.OrderDetailView.as_view()), name='detail'),
]