from django.urls import path

from orders.views import (CanceledView, OrderCreateView, OrderDetailView,
                          OrderListView, SuccessView)

app_name = 'orders'
urlpatterns = [
    path('orders_list/', OrderListView.as_view(), name='orders'),
    path('order_create/', OrderCreateView.as_view(), name='create_order'),
    path('order_success/', SuccessView.as_view(), name='order_success'),
    path('order_canceled/', CanceledView.as_view(), name='order_canceled'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
