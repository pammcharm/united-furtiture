from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "customer_name", "phone_number", "order_status", "payment_status", "created_at")
    list_editable = ("order_status", "payment_status")
    list_filter = ("order_status", "payment_status", "business")
    search_fields = ("customer__username", "customer__email", "customer_name", "phone_number", "delivery_location", "notes")
    date_hierarchy = "created_at"
    autocomplete_fields = ("business", "customer")
    save_on_top = True
    inlines = [OrderItemInline]
