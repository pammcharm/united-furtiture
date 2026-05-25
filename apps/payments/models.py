from django.db import models

from apps.businesses.models import Business


class PaymentMethod(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="payment_methods")
    name = models.CharField(max_length=80)
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
