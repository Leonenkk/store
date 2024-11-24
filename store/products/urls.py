
from django.urls import path
from products.views import  basket_add, basket_remove, ProductsListView

app_name = 'products'
urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category<int:category_id>/',ProductsListView.as_view(), name='category'),#если в int передается category_id, то в функцию также category_id, никак иначе
    path('page<int:page>/',ProductsListView.as_view(), name='page'),
    path('baskets/add/<int:product_id>/',basket_add,name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]