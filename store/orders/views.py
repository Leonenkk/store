from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.WEBHOOK_SECRET_KEY


class OrderListView(TitleMixin, ListView):
    model = Order
    template_name = "orders/orders.html"
    title = "Store - заказы"
    queryset = Order.objects.all()
    ordering = ('created',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


@method_decorator(cache_page(60 * 15), name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = "orders/order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = f"Заказ №{self.object.id}"
        return context


class SuccessView(TitleMixin, TemplateView):
    template_name = "orders/success.html"
    title = "Store - Спасибо за заказ!"


class CanceledView(TitleMixin, TemplateView):
    template_name = "orders/cancel.html"
    title = "Store - Ошибка с оплатой!"


class OrderCreateView(TitleMixin, CreateView):
    model = Order
    template_name = "orders/order-create.html"
    title = "Store-Оформление заказа"
    form_class = OrderForm
    success_url = reverse_lazy("orders:create_order")

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        self.object.stripe_session_id = checkout_session.id
        self.object.save()
        return redirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        session_id = event['data']['object']['id']
        fulfill_checkout(session_id)

    return HttpResponse(status=200)


def fulfill_checkout(session_id):
    order = Order.objects.get(stripe_session_id=session_id)
    order.update_after_payment()
