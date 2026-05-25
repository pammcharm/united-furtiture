import "./styles.css";
import { animate, hover, inView, stagger } from "motion";
import { createIcons, icons } from "lucide";

createIcons({ icons });

animate(
  ".hero-reveal",
  { opacity: [0, 1], y: [24, 0], filter: ["blur(8px)", "blur(0px)"] },
  { duration: 0.8, delay: stagger(0.12), easing: [0.22, 1, 0.36, 1] },
);

inView(
  ".motion-card",
  (element) => {
    animate(element, { opacity: [0, 1], y: [28, 0] }, { duration: 0.6, easing: [0.22, 1, 0.36, 1] });
  },
  { margin: "0px 0px -100px 0px" },
);

document.querySelectorAll(".motion-card").forEach((card) => {
  hover(card, () => {
    animate(card, { y: -5 }, { duration: 0.2 });
    return () => animate(card, { y: 0 }, { duration: 0.2 });
  });
});

const formatRwf = (amount) => `${new Intl.NumberFormat("en-US").format(amount)} RWF`;

const productGrid = document.querySelector("[data-product-grid]");
const productCards = productGrid ? [...productGrid.querySelectorAll("[data-product-room]")] : [];
const resultCount = document.querySelector("[data-result-count]");
const emptyState = document.querySelector("[data-empty-state]");
const searchInput = document.querySelector("[data-search]");
const sortSelect = document.querySelector("[data-sort]");
const priceRange = document.querySelector("[data-price-range]");
const priceLabel = document.querySelector("[data-price-label]");
let activeFilter = "all";

const runMarketplaceFilters = () => {
  if (!productGrid) {
    return;
  }

  const query = searchInput?.value.trim().toLowerCase() || "";
  const maxPrice = Number(priceRange?.value || Number.MAX_SAFE_INTEGER);
  const checkedMaterials = [...document.querySelectorAll("[data-material]:checked")].map((item) => item.value);

  const sortedCards = [...productCards].sort((a, b) => {
    const sort = sortSelect?.value || "featured";
    if (sort === "price-low") return Number(a.dataset.productPrice) - Number(b.dataset.productPrice);
    if (sort === "price-high") return Number(b.dataset.productPrice) - Number(a.dataset.productPrice);
    if (sort === "name") return a.dataset.productName.localeCompare(b.dataset.productName);
    return productCards.indexOf(a) - productCards.indexOf(b);
  });

  sortedCards.forEach((card) => productGrid.appendChild(card));

  let visibleCount = 0;
  sortedCards.forEach((card) => {
    const haystack = `${card.dataset.productName} ${card.dataset.productMaterial} ${card.dataset.productCategory}`.toLowerCase();
    const material = card.dataset.productMaterial.toLowerCase();
    const roomMatch = activeFilter === "all" || card.dataset.productRoom === activeFilter;
    const queryMatch = !query || haystack.includes(query);
    const priceMatch = Number(card.dataset.productPrice) <= maxPrice;
    const materialMatch = checkedMaterials.length === 0 || checkedMaterials.some((item) => material.includes(item));
    const visible = roomMatch && queryMatch && priceMatch && materialMatch;

    if (visible) {
      visibleCount += 1;
      card.hidden = false;
      animate(card, { opacity: [0.2, 1], scale: [0.98, 1], y: [10, 0], filter: "grayscale(0)" }, { duration: 0.26 });
    } else {
      animate(card, { opacity: 0, scale: 0.96 }, { duration: 0.18 }).finished.then(() => {
        card.hidden = true;
      });
    }
  });

  if (resultCount) resultCount.textContent = visibleCount;
  if (emptyState) emptyState.classList.toggle("hidden", visibleCount !== 0);
  if (priceLabel && priceRange) priceLabel.textContent = formatRwf(Number(priceRange.value));
};

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach((item) => item.classList.remove("is-active"));
    button.classList.add("is-active");
    runMarketplaceFilters();
  });
});

searchInput?.addEventListener("input", runMarketplaceFilters);
sortSelect?.addEventListener("change", runMarketplaceFilters);
priceRange?.addEventListener("input", runMarketplaceFilters);
document.querySelectorAll("[data-material]").forEach((input) => input.addEventListener("change", runMarketplaceFilters));
document.querySelector("[data-clear-filters]")?.addEventListener("click", () => {
  activeFilter = "all";
  document.querySelectorAll("[data-filter]").forEach((item) => item.classList.toggle("is-active", item.dataset.filter === "all"));
  if (searchInput) searchInput.value = "";
  if (sortSelect) sortSelect.value = "featured";
  if (priceRange) priceRange.value = priceRange.max;
  document.querySelectorAll("[data-material]").forEach((input) => {
    input.checked = false;
  });
  runMarketplaceFilters();
});
runMarketplaceFilters();

document.querySelectorAll("[data-slider]").forEach((slider) => {
  const slides = [...slider.querySelectorAll("[data-slide]")];
  const dots = [...slider.querySelectorAll("[data-slide-dot]")];
  let activeIndex = 0;

  if (slides.length < 2) {
    return;
  }

  const showSlide = (nextIndex) => {
    const currentSlide = slides[activeIndex];
    const nextSlide = slides[nextIndex];

    dots[activeIndex]?.classList.remove("is-active");
    dots[nextIndex]?.classList.add("is-active");
    nextSlide.classList.add("is-active");

    animate(currentSlide, { opacity: [1, 0], scale: [1, 1.02] }, { duration: 0.55, easing: [0.22, 1, 0.36, 1] }).finished.then(() => {
      currentSlide.classList.remove("is-active");
    });

    animate(nextSlide, { opacity: [0, 1], scale: [0.98, 1] }, { duration: 0.7, easing: [0.22, 1, 0.36, 1] });
    animate(nextSlide.querySelector(".showroom-caption"), { x: [28, 0], opacity: [0, 1] }, { duration: 0.65, delay: 0.08 });

    activeIndex = nextIndex;
  };

  let timer = window.setInterval(() => {
    showSlide((activeIndex + 1) % slides.length);
  }, 4200);

  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const nextIndex = Number(dot.dataset.slideDot);
      if (nextIndex === activeIndex) {
        return;
      }
      window.clearInterval(timer);
      showSlide(nextIndex);
      timer = window.setInterval(() => {
        showSlide((activeIndex + 1) % slides.length);
      }, 4200);
    });
  });
});

const updateCartTotals = () => {
  const items = [...document.querySelectorAll("[data-cart-item]")];
  if (!items.length) {
    return;
  }

  const subtotal = items.reduce((sum, item) => {
    const price = Number(item.dataset.itemPrice);
    const qty = Number(item.querySelector("[data-qty]").value);
    const itemTotal = price * qty;
    item.querySelector("[data-item-total]").textContent = formatRwf(itemTotal);
    return sum + itemTotal;
  }, 0);

  const delivery = 10000;
  document.querySelector("[data-cart-subtotal]").textContent = formatRwf(subtotal);
  document.querySelector("[data-cart-total]").textContent = formatRwf(subtotal + delivery);
};

document.querySelectorAll("[data-cart-item]").forEach((item) => {
  const qtyInput = item.querySelector("[data-qty]");
  item.querySelector("[data-qty-minus]")?.addEventListener("click", () => {
    qtyInput.value = Math.max(1, Number(qtyInput.value) - 1);
    animate(item, { scale: [1, 0.99, 1] }, { duration: 0.2 });
    updateCartTotals();
  });
  item.querySelector("[data-qty-plus]")?.addEventListener("click", () => {
    qtyInput.value = Math.min(20, Number(qtyInput.value) + 1);
    animate(item, { scale: [1, 1.01, 1] }, { duration: 0.2 });
    updateCartTotals();
  });
});
updateCartTotals();

document.querySelectorAll(".option-card").forEach((card) => {
  card.addEventListener("click", () => {
    const input = card.querySelector("input");
    document.querySelectorAll(`input[name="${input.name}"]`).forEach((radio) => {
      radio.closest(".option-card").classList.toggle("is-active", radio === input);
    });
  });
});

const orderForm = document.querySelector("[data-order-form]");
const orderWhatsapp = document.querySelector("[data-order-whatsapp]");
const whatsappPhone = "250785211404";
const locationInput = document.querySelector("[data-order-location]");
const shippingEstimate = document.querySelector("[data-shipping-estimate]");
const deliveryAreasScript = document.querySelector("#delivery-areas-data");
const deliveryAreas = deliveryAreasScript ? JSON.parse(deliveryAreasScript.textContent) : [];

const buildWhatsappWebUrl = (message) => `https://wa.me/${whatsappPhone}?text=${encodeURIComponent(message)}`;
const buildWhatsappAppUrl = (message) => `whatsapp://send?phone=${whatsappPhone}&text=${encodeURIComponent(message)}`;

const openWhatsapp = (message, webUrl) => {
  const fallbackUrl = webUrl || buildWhatsappWebUrl(message);
  const appUrl = buildWhatsappAppUrl(message);
  const startedAt = Date.now();
  window.location.href = appUrl;

  window.setTimeout(() => {
    if (Date.now() - startedAt < 1800 && document.visibilityState === "visible") {
      window.location.href = fallbackUrl;
    }
  }, 950);
};

const updateOrderMessage = () => {
  if (!orderForm || !orderWhatsapp) {
    return;
  }

  const name = orderForm.querySelector("[data-order-name]").value || "Customer";
  const phone = orderForm.querySelector("[data-order-phone]").value || "Not provided";
  const location = orderForm.querySelector("[data-order-location]").value || "Not provided";
  const delivery = orderForm.querySelector('input[name="delivery"]:checked')?.value || "Pickup from showroom";
  const payment = orderForm.querySelector('input[name="payment"]:checked')?.value || "Cash on delivery";
  const notes = orderForm.querySelector("[data-order-notes]").value || "No notes";
  const message = `Hello United Furniture, I want to place an order.\nName: ${name}\nPhone: ${phone}\nLocation: ${location}\nDelivery: ${delivery}\nPayment: ${payment}\nNotes: ${notes}`;
  orderWhatsapp.href = buildWhatsappWebUrl(message);
  orderWhatsapp.dataset.whatsappMessage = message;
};

orderForm?.addEventListener("input", updateOrderMessage);
orderForm?.addEventListener("change", updateOrderMessage);
updateOrderMessage();

const findDeliveryArea = (locationValue) => {
  const normalized = locationValue.toLowerCase();
  return (
    deliveryAreas.find((area) => {
      const keywords = `${area.name},${area.keywords || ""}`
        .toLowerCase()
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
      return keywords.some((keyword) => normalized.includes(keyword));
    }) ||
    deliveryAreas.find((area) => !area.name.toLowerCase().includes("pickup")) ||
    deliveryAreas[0]
  );
};

const updateShippingEstimate = () => {
  if (!shippingEstimate || !locationInput || deliveryAreas.length === 0) {
    return;
  }

  const locationValue = locationInput.value.trim();
  if (!locationValue) {
    shippingEstimate.textContent = "Enter your location to see delivery fee and estimated shipping time.";
    return;
  }

  const area = findDeliveryArea(locationValue);
  const fee = formatRwf(Number(area.fee || 0));
  shippingEstimate.textContent = `${area.name}: delivery fee ${fee}. Estimated shipping time ${area.estimated_min_days}-${area.estimated_max_days} day(s).`;
};

document.querySelector("[data-use-location]")?.addEventListener("click", () => {
  if (!navigator.geolocation || !locationInput) {
    if (shippingEstimate) shippingEstimate.textContent = "Location detection is not available in this browser. Please type your location.";
    return;
  }

  if (shippingEstimate) shippingEstimate.textContent = "Detecting your location...";
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      locationInput.value = `Current location: ${latitude.toFixed(5)}, ${longitude.toFixed(5)}`;
      updateShippingEstimate();
      updateOrderMessage();
    },
    () => {
      if (shippingEstimate) shippingEstimate.textContent = "We could not access your location. Please allow location permission or type your address.";
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 },
  );
});

locationInput?.addEventListener("input", updateShippingEstimate);
updateShippingEstimate();

document.querySelectorAll('a[href*="wa.me"], a[data-order-whatsapp]').forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    const url = new URL(link.href);
    const message = link.dataset.whatsappMessage || url.searchParams.get("text") || "Hello United Furniture, I want to order.";
    openWhatsapp(message, link.href);
  });
});
