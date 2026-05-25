from apps.businesses.models import Business
from apps.catalog.models import Product


BUSINESS = {
    "name": "United Furniture",
    "short_name": "United",
    "whatsapp_number": "250785211404",
    "phone_numbers": "0785 211 404 / 0780 313 287",
    "instagram_url": "https://www.instagram.com/unitedfurniture_rwanda/?hl=en",
    "location": "Kigali showroom",
    "currency": "RWF",
    "hero_image": "https://images.pexels.com/photos/276583/pexels-photo-276583.jpeg?auto=compress&cs=tinysrgb&w=1800",
}

CATEGORIES = [
    {"name": "Sofas", "slug": "sofas", "room": "living"},
    {"name": "Beds", "slug": "beds", "room": "bedroom"},
    {"name": "Dining Tables", "slug": "dining", "room": "dining"},
    {"name": "Office Furniture", "slug": "office", "room": "office"},
]

PRODUCTS = [
    {
        "name": "Luxury Sofa",
        "slug": "luxury-sofa",
        "price": 350000,
        "category": "Sofas",
        "room_type": "living",
        "material": "Velvet",
        "color": "Emerald",
        "size": "3 seats",
        "description": "A deep, comfortable statement sofa built for modern living rooms and showroom-ready photos.",
        "image_url": "https://images.pexels.com/photos/1866149/pexels-photo-1866149.jpeg?auto=compress&cs=tinysrgb&w=900",
    },
    {
        "name": "Oak Platform Bed",
        "slug": "oak-platform-bed",
        "price": 420000,
        "category": "Beds",
        "room_type": "bedroom",
        "material": "Oak wood",
        "color": "Natural",
        "size": "Queen",
        "description": "A clean wooden platform bed with a warm natural finish and strong frame.",
        "image_url": "https://images.pexels.com/photos/1454806/pexels-photo-1454806.jpeg?auto=compress&cs=tinysrgb&w=900",
    },
    {
        "name": "Walnut Dining Set",
        "slug": "walnut-dining-set",
        "price": 610000,
        "category": "Dining Tables",
        "room_type": "dining",
        "material": "Walnut",
        "color": "Brown",
        "size": "6 chairs",
        "description": "A complete dining table set for family homes, apartments, and guest houses.",
        "image_url": "https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg?auto=compress&cs=tinysrgb&w=900",
    },
    {
        "name": "Studio Office Desk",
        "slug": "studio-office-desk",
        "price": 280000,
        "category": "Office Furniture",
        "room_type": "office",
        "material": "Engineered wood",
        "color": "Black oak",
        "size": "140 cm",
        "description": "A practical desk with cable space for home offices and business workstations.",
        "image_url": "https://images.pexels.com/photos/1957477/pexels-photo-1957477.jpeg?auto=compress&cs=tinysrgb&w=900",
    },
]


def money(amount):
    return f"{amount:,} {BUSINESS['currency']}"


def whatsapp_url(product=None):
    message = "Hello, I want to order from United Furniture."
    if product:
        message = f"Hello, I want this product: {product['name']} Price: {money(product['price'])}"
    return f"https://wa.me/{BUSINESS['whatsapp_number']}?text={message.replace(' ', '%20')}"


def _product_dict(product):
    data = {
        "name": product.name,
        "slug": product.slug,
        "price": product.display_price,
        "category": product.category.name if product.category else "Furniture",
        "room_type": product.room_type,
        "material": product.material,
        "color": product.color,
        "size": product.size,
        "description": product.description,
        "image_url": product.image_url,
        "id": product.id,
        "tags": ", ".join(product.tags.values_list("name", flat=True)),
    }
    data["formatted_price"] = money(data["price"])
    data["whatsapp_url"] = whatsapp_url(data)
    return data


def site_context():
    business = Business.objects.filter(slug="united-furniture", is_active=True).first()
    db_products = []
    categories = CATEGORIES
    current_business = BUSINESS.copy()

    if business:
        current_business = {
            "name": business.name,
            "short_name": business.name.split()[0],
            "whatsapp_number": business.whatsapp_number,
            "phone_numbers": "0785 211 404 / 0780 313 287",
            "instagram_url": business.instagram_url or BUSINESS["instagram_url"],
            "location": business.location,
            "currency": business.currency,
            "hero_image": business.hero_image_url or BUSINESS["hero_image"],
        }
        db_products = list(
            Product.objects.filter(business=business, status=Product.Status.ACTIVE)
            .select_related("category")
            .order_by("-is_featured", "-created_at")
        )
        categories = [
            {"name": category.name, "slug": category.slug, "room": category.slug}
            for category in business.categories.all()
        ] or CATEGORIES

    if db_products:
        products = [_product_dict(product) for product in db_products]
    else:
        products = [{**product, "formatted_price": money(product["price"]), "whatsapp_url": whatsapp_url(product)} for product in PRODUCTS]

    showroom_products = sorted(
        products,
        key=lambda product: (
            "premium" not in product.get("tags", "").lower(),
            -product["price"],
        ),
    )[:8]
    if len(showroom_products) < 4:
        showroom_products = sorted(products, key=lambda product: -product["price"])[:8]

    return {
        "business": current_business,
        "categories": categories,
        "products": products,
        "featured_products": products[:4],
        "showroom_products": showroom_products,
        "whatsapp_url": whatsapp_url(),
        "site_url": "http://localhost:8000",
    }
