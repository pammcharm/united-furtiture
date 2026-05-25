from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.models import CustomerProfile
from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.pages.site_data import site_context
from apps.shipping.models import DeliveryArea
from .models import Order, OrderItem


def checkout(request):
    context = site_context()
    profile = None
    if request.user.is_authenticated:
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request, "Your cart is empty. Add a product before placing an order.")
            return redirect("cart:detail")

        business = Business.objects.filter(slug="united-furniture").first()
        if not business:
            messages.error(request, "Business is not configured.")
            return redirect("orders:checkout")

        order = Order.objects.create(
            business=business,
            customer=request.user if request.user.is_authenticated else None,
            customer_name=request.POST.get("customer_name", ""),
            phone_number=request.POST.get("phone_number", ""),
            delivery_location=request.POST.get("delivery_location", ""),
            notes=request.POST.get("notes", ""),
        )
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart.get(str(product.id), 1),
                unit_price=product.display_price,
            )

        if profile:
            profile.phone_number = order.phone_number
            profile.delivery_location = order.delivery_location
            profile.preferred_delivery_method = request.POST.get("delivery", "")
            profile.preferred_payment_method = request.POST.get("payment", "")
            profile.notes = order.notes
            profile.save()

        request.session["cart"] = {}
        messages.success(request, f"Order #{order.pk} saved. You can finish confirmation on WhatsApp.")
        return redirect("orders:checkout")

    context["checkout_profile"] = profile
    context["delivery_areas"] = [
        {
            "name": area.name,
            "fee": area.fee,
            "keywords": area.keywords,
            "estimated_min_days": area.estimated_min_days,
            "estimated_max_days": area.estimated_max_days,
        }
        for area in DeliveryArea.objects.filter(is_active=True).order_by("fee")
    ]
    return render(request, "orders/checkout.html", context)
