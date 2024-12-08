from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from products.models import Product, ProductCategory


# Create your tests here.
class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)  # вспомогательный класс для доп методов
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/index.html')
        self.assertEqual(response.context_data['title'], 'Store')


class ProductsListViewTestCase(TestCase):
    fixtures = ['ProductCategory.json', 'Product.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_category(self):
        path = reverse('products:category', kwargs={'category_id': 1})
        response = self.client.get(path)
        category = ProductCategory.objects.first()

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'Store - Каталог')


