from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from products.models import Product, ProductCategory, Basket
from users.models import User


def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)  # передается номер стр которую надо отобразить
    context = {
        'title': 'Store - Каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product_add = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product_add)
    # user=request.users-взять то что принадлежит конкретному пользователю
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product_add, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
