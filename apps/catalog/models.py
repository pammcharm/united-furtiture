from django.db import models
from django.urls import reverse

from apps.businesses.models import Business


class Category(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=120)
    slug = models.SlugField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "categories"
        unique_together = ("business", "slug")

    def __str__(self):
        return self.name


class ProductTag(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="product_tags")
    name = models.CharField(max_length=80)
    slug = models.SlugField()

    class Meta:
        unique_together = ("business", "slug")

    def __str__(self):
        return self.name


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        SOLD_OUT = "sold_out", "Sold out"

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="products")
    name = models.CharField(max_length=160)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_featured = models.BooleanField(default=False)
    material = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=80, blank=True)
    size = models.CharField(max_length=100, blank=True)
    room_type = models.CharField(max_length=100, blank=True)
    furniture_type = models.CharField(max_length=100, blank=True)
    custom_order_available = models.BooleanField(default=False)
    tags = models.ManyToManyField(ProductTag, blank=True, related_name="products")
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.TextField(blank=True)
    image_alt_text = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("business", "slug")
        ordering = ("-is_featured", "-created_at")

    def __str__(self):
        return self.name

    @property
    def display_price(self):
        return self.discount_price or self.price

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})
