from django.db import models

from apps.businesses.models import Business


class DeliveryArea(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="delivery_areas")
    name = models.CharField(max_length=120)
    fee = models.PositiveIntegerField(default=0)
    keywords = models.CharField(max_length=240, blank=True, help_text="Comma-separated words to match customer location, e.g. kigali, gasabo, nyarutarama")
    estimated_min_days = models.PositiveIntegerField(default=1)
    estimated_max_days = models.PositiveIntegerField(default=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
