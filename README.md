# United Furniture Django Commerce

Reusable Django e-commerce project for United Furniture first, with apps that can later power other shops.

## Apps

- `accounts` - users, staff, owners, customers
- `businesses` - business profile, WhatsApp number, theme info
- `catalog` - categories and furniture products
- `cart` - cart page
- `orders` - checkout and order models
- `payments` - manual payment methods
- `shipping` - delivery areas and fees
- `pages` - homepage and shared site context

## Frontend

The templates are normal Django HTML templates. Tailwind, Lucide icons, and Motion animations are built with Node/Vite into:

- `static/dist/app.css`
- `static/dist/app.js`

## Run

```bash
npm install
npm run build
python manage.py migrate
python manage.py seed_united_furniture
python manage.py runserver
```

Open:

```text
http://localhost:8000/
```

Owner dashboard:

```text
http://localhost:8000/admin/
```

The admin dashboard is protected by Django login.

## Render Demo Deploy

This repo includes `render.yaml` for a free demo deployment. Render free web services can sleep after inactivity, so use a paid web service plan later when the shop must stay always online.
