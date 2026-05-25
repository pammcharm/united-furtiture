from django.contrib import admin

from .models import AdminPasswordResetRequired, CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "delivery_location", "preferred_delivery_method", "preferred_payment_method")
    search_fields = ("user__username", "user__email", "phone_number", "delivery_location")
    autocomplete_fields = ("user",)


@admin.register(AdminPasswordResetRequired)
class AdminPasswordResetRequiredAdmin(admin.ModelAdmin):
    list_display = ("user", "required", "created_at")
    list_editable = ("required",)
    search_fields = ("user__username", "user__email")
    autocomplete_fields = ("user",)
