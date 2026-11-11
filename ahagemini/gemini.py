import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# --- 1. PRODUCT MASTER (dim_products) ---
dim_products = pd.DataFrame([
    {
        "product_id": 1,
        "sku": "SKU-SAT-015",
        "product_name": "Instant Sattu Breakfast Premix (15 Sachets)",
        "category": "Breakfast / Protein",
        "routine_slot": "8:00 AM",
        "serving_format": "15 x 30g Sachets",
        "unit_price": 375,
        "cogs": 115,
        "packaging_labor": 35,
        "total_unit_cost": 150,
        "gross_margin_pct": 0.60
    },
    {
        "product_id": 2,
        "sku": "SKU-MAK-PER15",
        "product_name": "Roasted Peri Peri Makhana (15 Snack Sachets)",
        "category": "Snacks / Crunch",
        "routine_slot": "4:00 PM",
        "serving_format": "15 x 20g Sachets",
        "unit_price": 375,
        "cogs": 108,
        "packaging_labor": 42,
        "total_unit_cost": 150,
        "gross_margin_pct": 0.60
    },
    {
        "product_id": 3,
        "sku": "SKU-MAK-PEP15",
        "product_name": "Roasted Black Pepper Makhana (15 Snack Sachets)",
        "category": "Snacks / Crunch",
        "routine_slot": "4:00 PM",
        "serving_format": "15 x 20g Sachets",
        "unit_price": 375,
        "cogs": 104,
        "packaging_labor": 42,
        "total_unit_cost": 146,
        "gross_margin_pct": 0.61
    },
    {
        "product_id": 4,
        "sku": "SKU-MAK-MNT15",
        "product_name": "Roasted Mint / Pudina Makhana (15 Snack Sachets)",
        "category": "Snacks / Crunch",
        "routine_slot": "4:00 PM",
        "serving_format": "15 x 20g Sachets",
        "unit_price": 375,
        "cogs": 106,
        "packaging_labor": 42,
        "total_unit_cost": 148,
        "gross_margin_pct": 0.61
    },
    {
        "product_id": 5,
        "sku": "SKU-MAK-PHL250",
        "product_name": "Classic Phool Makhana - Plain / Raw (250g Jar)",
        "category": "Clean Staples",
        "routine_slot": "Family / Cooking",
        "serving_format": "250g Jar",
        "unit_price": 299,
        "cogs": 85,
        "packaging_labor": 25,
        "total_unit_cost": 110,
        "gross_margin_pct": 0.63
    },
    {
        "product_id": 6,
        "sku": "SKU-COM-84BOX",
        "product_name": "The 8 AM & 4 PM Workday Routine Box",
        "category": "Combo Box",
        "routine_slot": "Full Day Routine",
        "serving_format": "15 Sattu + 15 Assorted Makhana",
        "unit_price": 699,
        "cogs": 215,
        "packaging_labor": 65,
        "total_unit_cost": 280,
        "gross_margin_pct": 0.60
    }
])

# --- 2. CUSTOMER MASTER (dim_customers) ---
num_customers = 1200
first_names = ["Rohan", "Sneha", "Aditya", "Priya", "Arjun", "Kavita", "Vikram", "Ananya", "Rahul", "Pooja", "Amitabh", "Deepika"]
last_names = ["Mehta", "Sharma", "Verma", "Nair", "Deshmukh", "Iyer", "Sengupta", "Kulkarni", "Singhania", "Jha", "Reddy", "Saxena"]

target_cities = [
    ("Bengaluru", "Karnataka", 560001, 0.28),
    ("Gurugram", "Haryana", 122001, 0.16),
    ("Pune", "Maharashtra", 411001, 0.14),
    ("Hyderabad", "Telangana", 500001, 0.12),
    ("Mumbai", "Maharashtra", 400001, 0.12),
    ("Delhi", "Delhi", 110001, 0.08),
    ("Noida", "Uttar Pradesh", 201301, 0.05),
    ("Chennai", "Tamil Nadu", 600001, 0.05)
]

segments = ["Corporate Worker", "Athlete / Fitness", "Student / Aspirant", "Mom / Family"]
segment_weights = [0.60, 0.15, 0.12, 0.13]
channels = ["Meta Ads", "Google PMax", "Influencer", "Organic Search", "Word of Mouth"]
channel_weights = [0.45, 0.25, 0.15, 0.10, 0.05]

start_date = datetime(2025, 8, 1)
end_date = datetime(2026, 10, 31)
total_days = (end_date - start_date).days

customer_records = []
city_names = [c[0] for c in target_cities]
city_probs = [c[3] for c in target_cities]

for cid in range(101, 101 + num_customers):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    chosen_city_idx = np.random.choice(len(target_cities), p=city_probs)
    city, state, pin_base, _ = target_cities[chosen_city_idx]
    pincode = pin_base + random.randint(1, 80)
    segment = np.random.choice(segments, p=segment_weights)
    signup = start_date + timedelta(days=int(np.random.uniform(0, total_days - 10)))
    channel = np.random.choice(channels, p=channel_weights)
    
    customer_records.append({
        "customer_id": cid,
        "customer_name": name,
        "customer_segment": segment,
        "city": city,
        "state": state,
        "pincode": pincode,
        "signup_date": signup.strftime("%Y-%m-%d"),
        "acquisition_channel": channel
    })

dim_customers = pd.DataFrame(customer_records)
dim_customers['signup_dt'] = pd.to_datetime(dim_customers['signup_date'])

# --- 3. ORDERS & ORDER ITEMS (fact_orders & fact_order_items) ---
orders = []
order_items = []
order_id_counter = 10001
order_item_id = 1

for day_offset in range(total_days):
    cur_date = start_date + timedelta(days=day_offset)
    is_festive = cur_date.month in [10, 11]
    multiplier = 2.1 if is_festive else 1.0
    daily_order_count = int(np.random.poisson(lam=7.5 * multiplier))
    
    eligible_custs = dim_customers[dim_customers['signup_dt'] <= cur_date]
    if len(eligible_custs) == 0:
        continue

    for _ in range(daily_order_count):
        cust = eligible_custs.sample(1).iloc[0]
        status = np.random.choice(["Delivered", "Cancelled", "Returned (RTO)"], p=[0.92, 0.03, 0.05])
        payment_method = np.random.choice(["UPI", "Credit Card", "Debit Card", "Net Banking"], p=[0.74, 0.16, 0.07, 0.03])
        
        # Basket pattern: frequent 8 AM + 4 PM routine pairings
        basket_type = np.random.choice(["Single Sachet Pack", "8 & 4 Routine Pair", "Combo Routine Box", "Multi-Flavor Snack Pack"], p=[0.35, 0.35, 0.20, 0.10])
        
        selected_items = []
        if basket_type == "Single Sachet Pack":
            chosen_pid = np.random.choice([1, 2, 3, 4], p=[0.40, 0.25, 0.20, 0.15])
            selected_items.append((chosen_pid, 1))
        elif basket_type == "8 & 4 Routine Pair":
            # 1 Sattu (8 AM) + 1 Makhana (4 PM)
            makhana_pid = np.random.choice([2, 3, 4], p=[0.45, 0.30, 0.25])
            selected_items.append((1, 1))
            selected_items.append((makhana_pid, 1))
        elif basket_type == "Combo Routine Box":
            selected_items.append((6, 1))
        else: # Multi-Flavor Snack Pack
            selected_items.append((np.random.choice([2, 3, 4]), 1))
            selected_items.append((np.random.choice([2, 3, 4]), 1))

        gross = 0
        total_cogs = 0
        
        for pid, qty in selected_items:
            prod = dim_products[dim_products['product_id'] == pid].iloc[0]
            line_total = prod['unit_price'] * qty
            line_cogs = prod['total_unit_cost'] * qty
            gross += line_total
            total_cogs += line_cogs
            
            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order_id_counter,
                "product_id": pid,
                "quantity": qty,
                "unit_price": prod['unit_price'],
                "line_total": line_total,
                "line_cogs": line_cogs
            })
            order_item_id += 1

        discount = 50 if (gross >= 700 and random.random() > 0.4) else 0
        shipping = 0 if gross >= 500 else 49
        net = gross - discount + shipping
        
        if status == "Cancelled":
            delivery_days = 0
        elif cust['city'] in ["Bengaluru", "Pune", "Hyderabad", "Mumbai", "Chennai"]:
            delivery_days = int(np.random.choice([3, 4, 5], p=[0.50, 0.40, 0.10]))
        else:
            delivery_days = int(np.random.choice([2, 3, 4], p=[0.60, 0.35, 0.05]))

        orders.append({
            "order_id": order_id_counter,
            "customer_id": cust['customer_id'],
            "order_date": cur_date.strftime("%Y-%m-%d"),
            "order_status": status,
            "payment_method": payment_method,
            "gross_amount": gross,
            "discount_amount": discount,
            "shipping_fee": shipping,
            "net_amount": net,
            "order_cogs": total_cogs,
            "delivery_days": delivery_days
        })
        order_id_counter += 1

fact_orders = pd.DataFrame(orders)
fact_order_items = pd.DataFrame(order_items)

# --- 4. MARKETING SPEND (fact_marketing_spend) ---
marketing = []
spend_id = 1

for day_offset in range(total_days):
    cur_date = start_date + timedelta(days=day_offset)
    is_festive = cur_date.month in [10, 11]
    
    # 8 AM Sattu Ad Campaign
    sattu_spend = random.randint(2200, 3600) if is_festive else random.randint(1100, 1600)
    sattu_clicks = int(sattu_spend / random.uniform(5.5, 7.2))
    marketing.append({
        "spend_id": spend_id,
        "date": cur_date.strftime("%Y-%m-%d"),
        "channel": "Meta Ads",
        "target_routine": "8 AM Breakfast Sattu",
        "spend_inr": sattu_spend,
        "impressions": sattu_clicks * random.randint(35, 45),
        "clicks": sattu_clicks,
        "attributed_orders": int(sattu_clicks * random.uniform(0.025, 0.040))
    })
    spend_id += 1

    # 4 PM Makhana Ad Campaign
    mak_spend = random.randint(2400, 3800) if is_festive else random.randint(1200, 1800)
    mak_clicks = int(mak_spend / random.uniform(5.8, 7.5))
    marketing.append({
        "spend_id": spend_id,
        "date": cur_date.strftime("%Y-%m-%d"),
        "channel": "Meta Ads",
        "target_routine": "4 PM Desk Makhana",
        "spend_inr": mak_spend,
        "impressions": mak_clicks * random.randint(36, 46),
        "clicks": mak_clicks,
        "attributed_orders": int(mak_clicks * random.uniform(0.026, 0.042))
    })
    spend_id += 1

    # Google PMax (Brand / Combo Routine Box)
    pmax_spend = random.randint(1400, 2200) if is_festive else random.randint(700, 1200)
    pmax_clicks = int(pmax_spend / random.uniform(7.0, 9.2))
    marketing.append({
        "spend_id": spend_id,
        "date": cur_date.strftime("%Y-%m-%d"),
        "channel": "Google PMax",
        "target_routine": "Brand / Combo Box",
        "spend_inr": pmax_spend,
        "impressions": pmax_clicks * random.randint(26, 36),
        "clicks": pmax_clicks,
        "attributed_orders": int(pmax_clicks * random.uniform(0.030, 0.048))
    })
    spend_id += 1

fact_marketing_spend = pd.DataFrame(marketing)

# Export all CSV files
dim_products.to_csv("dim_products.csv", index=False)
dim_customers.drop(columns=['signup_dt']).to_csv("dim_customers.csv", index=False)
fact_orders.to_csv("fact_orders.csv", index=False)
fact_order_items.to_csv("fact_order_items.csv", index=False)
fact_marketing_spend.to_csv("fact_marketing_spend.csv", index=False)

print(f"Generated {len(dim_products)} products, {len(dim_customers)} customers, {len(fact_orders)} orders, {len(fact_order_items)} items, and {len(fact_marketing_spend)} marketing records.")