from django import template
from cors.models import Order

register = template.Library()

# this will allow us to load our method in any page so now you will display this count if is authenticated user come
@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

