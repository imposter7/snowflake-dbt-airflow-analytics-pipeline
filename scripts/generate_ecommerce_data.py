
from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd
from faker import Faker

# Reproducible synthetic data
random.seed(42)
Faker.seed(42)
fake = Faker("en_US")

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Customers
customers = []
for customer_id in range(1, 1001):
    customers.append({
        "customer_id": customer_id,
        "customer_name": fake.name(),
        "email": f"customer{customer_id}@example.com",
        "city": fake.city(),
        "state": fake.state_abbr(),
        "signup_date": fake.date_between(
            start_date="-3y", end_date="-1y"
        ).isoformat()
    })

# 2. Products
categories = {
    "Electronics": ["Headphones", "Keyboard", "Mouse", "Webcam"],
    "Home": ["Lamp", "Blender", "Coffee Maker", "Chair"],
    "Clothing": ["T-Shirt", "Jacket", "Jeans", "Sweater"],
    "Sports": ["Yoga Mat", "Water Bottle", "Dumbbells", "Backpack"]
}

products = []
for product_id in range(1, 201):
    category = random.choice(list(categories))
    product_name = random.choice(categories[category])

    products.append({
        "product_id": product_id,
        "product_name": f"{product_name} {product_id}",
        "category": category,
        "unit_price": round(random.uniform(10, 500), 2)
    })

# 3. Orders and order items
orders = []
order_items = []
item_id = 1

for order_id in range(1, 5001):
    order_date = datetime(2025, 1, 1) + timedelta(
        days=random.randint(0, 620)
    )

    status = random.choices(
        ["completed", "shipped", "cancelled", "returned"],
        weights=[65, 20, 10, 5]
    )[0]

    orders.append({
        "order_id": order_id,
        "customer_id": random.randint(1, 1000),
        "order_date": order_date.date().isoformat(),
        "order_status": status
    })

    selected_products = random.sample(
        products, k=random.randint(1, 4)
    )

    for product in selected_products:
        order_items.append({
            "order_item_id": item_id,
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": random.randint(1, 3),
            "unit_price": product["unit_price"]
        })
        item_id += 1

datasets = {
    "customers": customers,
    "products": products,
    "orders": orders,
    "order_items": order_items
}

for name, records in datasets.items():
    path = OUTPUT_DIR / f"{name}.csv"
    pd.DataFrame(records).to_csv(path, index=False)
    print(f"Created {path.name}: {len(records):,} rows")

print("\nAll e-commerce datasets generated successfully!")

