from django.db import models

from products.models import Basket, BasketQuerySet
from users.models import User


class Order(models.Model):  # сделать модель Address,а поле адрес в Order заполнять через ForeignKey
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'создан'),
        (PAID, 'оплачен'),
        (ON_WAY, 'в пути'),
        (DELIVERED, 'доставлен'),
    )
    
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    basket_history = models.JSONField(default=dict)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUSES, default=CREATED)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order#{self.id} {self.first_name} {self.last_name}"

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = Order.PAID
        self.basket_history = {
            'basket_items': [basket.de_json() for basket in baskets],
            'total_price': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()

# ADD CLASS META(verbose_name,verbose_nam`1e_plural) AND CHECK OTHER COMPONENTS FOR META
