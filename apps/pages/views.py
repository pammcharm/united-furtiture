from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .site_data import site_context


def home(request):
    return render(request, "pages/home.html", site_context())


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri(reverse('pages:sitemap'))}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap(request):
    context = site_context()
    base_url = request.build_absolute_uri("/").rstrip("/")
    urls = [
        {"loc": base_url + reverse("pages:home"), "priority": "1.0"},
        {"loc": base_url + reverse("catalog:shop"), "priority": "0.9"},
        {"loc": base_url + reverse("cart:detail"), "priority": "0.3"},
        {"loc": base_url + reverse("orders:checkout"), "priority": "0.3"},
    ]
    for product in context["products"]:
        urls.append({"loc": base_url + reverse("catalog:product_detail", kwargs={"slug": product["slug"]}), "priority": "0.8"})
    xml = render(request, "pages/sitemap.xml", {"urls": urls}, content_type="application/xml")
    return xml
