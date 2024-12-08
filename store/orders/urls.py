from django.urls import path
from orders.views import OrderListView, OrderCreateView

app_name = 'orders'
urlpatterns = [
    path('orders_list/', OrderListView.as_view(), name='orders'),
    path('order_create/', OrderCreateView.as_view(), name='create_order'),
]
