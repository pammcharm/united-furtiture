from django.core.management.base import BaseCommand

from apps.businesses.models import Business
from apps.catalog.models import Category, Product, ProductTag
from apps.payments.models import PaymentMethod
from apps.shipping.models import DeliveryArea


class Command(BaseCommand):
    help = "Create sample United Furniture business, categories, products, payments, and delivery areas."

    def handle(self, *args, **options):
        business, _ = Business.objects.update_or_create(
            slug="united-furniture",
            defaults={
                "name": "United Furniture",
                "logo_url": "/static/brand/logo.png",
                "whatsapp_number": "250785211404",
                "instagram_url": "https://www.instagram.com/unitedfurniture_rwanda/?hl=en",
                "location": "Kigali showroom",
                "currency": "RWF",
                "primary_color": "#10b981",
                "hero_image_url": "https://images.pexels.com/photos/276583/pexels-photo-276583.jpeg?auto=compress&cs=tinysrgb&w=1800",
                "is_active": True,
            },
        )

        product_data = [
            ("Luxury Sofa", "luxury-sofa", "Sofas", "living", "Velvet", "Emerald", "3 seats", 350000, "https://images.pexels.com/photos/1866149/pexels-photo-1866149.jpeg?auto=compress&cs=tinysrgb&w=900", ["featured", "soft", "modern"]),
            ("Cloud Sectional Sofa", "cloud-sectional-sofa", "Sofas", "living", "Boucle", "Cream", "L shape", 720000, "https://images.pexels.com/photos/6585758/pexels-photo-6585758.jpeg?auto=compress&cs=tinysrgb&w=900", ["premium", "family", "modern"]),
            ("Compact Apartment Sofa", "compact-apartment-sofa", "Sofas", "living", "Linen", "Grey", "2 seats", 240000, "https://images.pexels.com/photos/276528/pexels-photo-276528.jpeg?auto=compress&cs=tinysrgb&w=900", ["small-space", "affordable"]),
            ("Oak Platform Bed", "oak-platform-bed", "Beds", "bedroom", "Oak wood", "Natural", "Queen", 420000, "https://images.pexels.com/photos/1454806/pexels-photo-1454806.jpeg?auto=compress&cs=tinysrgb&w=900", ["wood", "bedroom"]),
            ("Upholstered Storage Bed", "upholstered-storage-bed", "Beds", "bedroom", "Fabric", "Charcoal", "King", 560000, "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&w=900", ["storage", "premium"]),
            ("Kids Single Bed", "kids-single-bed", "Beds", "bedroom", "Pine wood", "White", "Single", 180000, "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&w=900", ["kids", "affordable"]),
            ("Walnut Dining Set", "walnut-dining-set", "Dining Tables", "dining", "Walnut", "Brown", "6 chairs", 610000, "https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg?auto=compress&cs=tinysrgb&w=900", ["wood", "family"]),
            ("Round Marble Dining Table", "round-marble-dining-table", "Dining Tables", "dining", "Marble", "White", "4 chairs", 480000, "https://images.pexels.com/photos/6580227/pexels-photo-6580227.jpeg?auto=compress&cs=tinysrgb&w=900", ["premium", "modern"]),
            ("Studio Office Desk", "studio-office-desk", "Office Furniture", "office", "Engineered wood", "Black oak", "140 cm", 280000, "https://images.pexels.com/photos/1957477/pexels-photo-1957477.jpeg?auto=compress&cs=tinysrgb&w=900", ["office", "work"]),
            ("Executive Office Chair", "executive-office-chair", "Office Furniture", "office", "Leather", "Black", "Adjustable", 220000, "https://images.pexels.com/photos/586996/pexels-photo-586996.jpeg?auto=compress&cs=tinysrgb&w=900", ["office", "ergonomic"]),
            ("Sliding Door Wardrobe", "sliding-door-wardrobe", "Wardrobes", "bedroom", "MDF", "Walnut", "220 cm", 530000, "https://images.pexels.com/photos/6782466/pexels-photo-6782466.jpeg?auto=compress&cs=tinysrgb&w=900", ["storage", "wood"]),
            ("Minimal TV Stand", "minimal-tv-stand", "TV Stands", "living", "Oak veneer", "Natural", "180 cm", 260000, "https://images.pexels.com/photos/5998138/pexels-photo-5998138.jpeg?auto=compress&cs=tinysrgb&w=900", ["living", "modern"]),
            ("Accent Lounge Chair", "accent-lounge-chair", "Chairs", "living", "Velvet", "Mustard", "Single", 190000, "https://images.pexels.com/photos/276534/pexels-photo-276534.jpeg?auto=compress&cs=tinysrgb&w=900", ["accent", "color"]),
            ("Rattan Coffee Table", "rattan-coffee-table", "Home Decor", "living", "Rattan", "Natural", "90 cm", 150000, "https://images.pexels.com/photos/6207807/pexels-photo-6207807.jpeg?auto=compress&cs=tinysrgb&w=900", ["decor", "natural"]),
            ("Entryway Console", "entryway-console", "Home Decor", "living", "Metal and wood", "Black", "120 cm", 175000, "https://images.pexels.com/photos/6312354/pexels-photo-6312354.jpeg?auto=compress&cs=tinysrgb&w=900", ["decor", "entryway"]),
        ]

        categories = {}
        for _, _, category_name, *_ in product_data:
            category, _ = Category.objects.update_or_create(
                business=business,
                slug=category_name.lower().replace(" ", "-"),
                defaults={"name": category_name, "is_featured": True},
            )
            categories[category_name] = category

        tags = {}
        for *_, tag_names in product_data:
            for tag_name in tag_names:
                tag, _ = ProductTag.objects.update_or_create(
                    business=business,
                    slug=tag_name,
                    defaults={"name": tag_name.replace("-", " ").title()},
                )
                tags[tag_name] = tag

        for name, slug, category_name, room_type, material, color, size, price, image_url, tag_names in product_data:
            product, _ = Product.objects.update_or_create(
                business=business,
                slug=slug,
                defaults={
                    "category": categories[category_name],
                    "name": name,
                    "description": f"{name} for {room_type} spaces, made with {material.lower()} and finished in {color.lower()}.",
                    "image_url": image_url,
                    "price": price,
                    "stock": 8 + (price % 7),
                    "status": Product.Status.ACTIVE,
                    "is_featured": slug in {"luxury-sofa", "oak-platform-bed", "walnut-dining-set", "studio-office-desk"},
                    "material": material,
                    "color": color,
                    "size": size,
                    "room_type": room_type,
                    "furniture_type": category_name,
                    "custom_order_available": True,
                    "seo_title": name,
                    "seo_description": f"Buy {name} from United Furniture.",
                    "image_alt_text": name,
                },
            )
            product.tags.set(tags[tag_name] for tag_name in tag_names)

        for name, instructions in {
            "Cash on delivery": "Pay when your order is delivered.",
            "Bank transfer": "Send payment reference after transfer.",
            "Mobile money": "Send manual mobile money reference.",
        }.items():
            PaymentMethod.objects.update_or_create(
                business=business,
                name=name,
                defaults={"instructions": instructions, "is_active": True},
            )

        delivery_areas = {
            "Pickup": (0, "pickup, showroom, store", 0, 0),
            "Kigali delivery": (10000, "kigali, gasabo, kicukiro, nyarugenge, remera, kimironko, nyarutarama", 1, 2),
            "Outside Kigali": (25000, "musanze, huye, rubavu, rusizi, muhanga, rwanda", 2, 5),
        }
        for name, (fee, keywords, min_days, max_days) in delivery_areas.items():
            DeliveryArea.objects.update_or_create(
                business=business,
                name=name,
                defaults={
                    "fee": fee,
                    "keywords": keywords,
                    "estimated_min_days": min_days,
                    "estimated_max_days": max_days,
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("United Furniture sample data is ready."))
