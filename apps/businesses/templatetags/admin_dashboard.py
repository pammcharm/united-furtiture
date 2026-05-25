from django import template
from django.db.models import Sum

from apps.businesses.models import Business
from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem

register = template.Library()


@register.simple_tag
def united_admin_stats():
    order_total = OrderItem.objects.aggregate(total=Sum("unit_price"))["total"] or 0
    return {
        "businesses": Business.objects.count(),
        "products": Product.objects.count(),
        "active_products": Product.objects.filter(status=Product.Status.ACTIVE).count(),
        "categories": Category.objects.count(),
        "orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(order_status=Order.OrderStatus.PENDING).count(),
        "sales": order_total,
    }
