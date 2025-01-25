import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    stripe_product_price_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'Продукт {self.name} | Категория {self.category}'

    def save(self, *args, **kwargs):
        if not self.stripe_product_price_id:
            try:
                stripe_product_price = self.create_stripe_product_price()
                self.stripe_product_price_id = stripe_product_price['id']
            except stripe.error.StripeError as e:
                raise ValueError(f"Ошибка Stripe API: {e}")
        else:
            stripe.Product.modify(
                self.stripe_product_price_id,
                name=self.name,
            )
        super().save(*args, **kwargs)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price_id = stripe.Price.create(product=stripe_product['id'], unit_amount=round(self.price * 100),
                                                      currency='rub')
        return stripe_product_price_id


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)  # добавление и сохранение будет проходить автоматически
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"User: {self.user.username}, Product: {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item={
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price':float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item
# для Basket можно было сделать @property, а не создавать класс BasketQuerySet
