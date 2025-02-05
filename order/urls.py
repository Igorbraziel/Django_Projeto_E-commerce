from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('payment/<int:pk>/', views.PaymentView.as_view(), name='payment'),
    path('closeorder/', views.CloseOrderView.as_view(), name='closeorder'),
    path('list/', views.OrderListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.OrderDetailView.as_view(), name='detail'),
]