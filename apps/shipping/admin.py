from django.contrib import admin

from .models import DeliveryArea


@admin.register(DeliveryArea)
class DeliveryAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "fee", "estimated_min_days", "estimated_max_days", "is_active")
    list_editable = ("fee", "estimated_min_days", "estimated_max_days", "is_active")
    search_fields = ("name", "keywords")
    list_filter = ("business", "is_active")
