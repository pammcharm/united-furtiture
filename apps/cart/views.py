from django.shortcuts import get_object_or_404, redirect, render

from apps.catalog.models import Product
from apps.pages.site_data import site_context


def _cart(request):
    return request.session.setdefault("cart", {})


def cart_detail(request):
    context = site_context()
    cart = _cart(request)
    products = Product.objects.filter(id__in=cart.keys()).select_related("category")
    cart_items = []
    total = 0
    for product in products:
        quantity = cart.get(str(product.id), 1)
        item_total = product.display_price * quantity
        total += item_total
        cart_items.append(
            {
                "id": product.id,
                "slug": product.slug,
                "name": product.name,
                "price": product.display_price,
                "quantity": quantity,
                "item_total": item_total,
                "formatted_price": f"{product.display_price:,} {context['business']['currency']}",
                "formatted_total": f"{item_total:,} {context['business']['currency']}",
                "image_url": product.image_url,
                "material": product.material,
                "size": product.size,
            }
        )
    context["cart_items"] = cart_items
    context["cart_total"] = f"{total:,} {context['business']['currency']}"
    context["cart_total_raw"] = total
    return render(request, "cart/cart_detail.html", context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, status=Product.Status.ACTIVE)
    cart = _cart(request)
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session.modified = True
    return redirect("cart:detail")


def remove_from_cart(request, product_id):
    cart = _cart(request)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect("cart:detail")


def update_cart(request, product_id):
    cart = _cart(request)
    quantity = max(1, int(request.POST.get("quantity", 1)))
    cart[str(product_id)] = quantity
    request.session.modified = True
    return redirect("cart:detail")
