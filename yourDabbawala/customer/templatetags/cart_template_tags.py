from django import template
from restaurant.models import Order

register = template.Library()

@register.filter
def cart_items_count(request):
    order_id = request.session.get('order_id', None)
    if order_id:
        order = Order.objects.get(id=order_id)
        return order.total_cart_items
    else:
        return 0