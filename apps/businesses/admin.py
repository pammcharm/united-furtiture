from django.contrib import admin

from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("name", "whatsapp_number", "currency", "is_active")
    list_editable = ("whatsapp_number", "currency", "is_active")
    list_filter = ("is_active", "currency")
    search_fields = ("name", "whatsapp_number", "location", "domain_name")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Business identity", {"fields": ("name", "slug", "logo_url", "hero_image_url", "is_active")}),
        ("Contact and location", {"fields": ("whatsapp_number", "location", "domain_name")}),
        ("Theme and money", {"fields": ("primary_color", "currency")}),
        ("Social links", {"fields": ("instagram_url", "facebook_url"), "classes": ("collapse",)}),
    )
