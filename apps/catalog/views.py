from django.http import Http404
from django.shortcuts import render

from apps.pages.site_data import PRODUCTS, site_context


def shop(request):
    context = site_context()
    return render(request, "catalog/shop.html", context)


def product_detail(request, slug):
    context = site_context()
    product = next((item for item in context["products"] if item["slug"] == slug), None)
    if product is None:
        raise Http404("Product not found")
    context["product"] = product
    context["related_products"] = [item for item in context["products"] if item["slug"] != slug][:3]
    return render(request, "catalog/product_detail.html", context)
