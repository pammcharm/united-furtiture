from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    logo_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=30)
    location = models.CharField(max_length=180, blank=True)
    currency = models.CharField(max_length=10, default="RWF")
    primary_color = models.CharField(max_length=20, default="#10b981")
    domain_name = models.CharField(max_length=120, blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    hero_image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "businesses"

    def __str__(self):
        return self.name
