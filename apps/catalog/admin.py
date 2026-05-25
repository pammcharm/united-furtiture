from django.contrib import admin

from .models import Category, Product, ProductTag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "is_featured")
    list_editable = ("is_featured",)
    list_filter = ("business", "is_featured")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ("name", "business")
    list_filter = ("business",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "category", "price", "stock", "status", "is_featured", "custom_order_available")
    list_editable = ("price", "stock", "status", "is_featured", "custom_order_available")
    list_filter = ("business", "category", "tags", "status", "is_featured", "room_type", "material", "custom_order_available")
    search_fields = ("name", "description", "material", "color", "room_type", "furniture_type")
    autocomplete_fields = ("business", "category")
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    fieldsets = (
        ("Product", {"fields": ("business", "category", "name", "slug", "description", "image_url")}),
        ("Pricing and stock", {"fields": ("price", "discount_price", "stock", "status", "is_featured")}),
        ("Furniture details", {"fields": ("material", "color", "size", "room_type", "furniture_type", "custom_order_available", "tags")}),
        ("SEO", {"fields": ("seo_title", "seo_description", "image_alt_text"), "classes": ("collapse",)}),
    )
